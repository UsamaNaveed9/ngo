
# -*- coding: utf-8 -*-
# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe import _, msgprint
from fuzzywuzzy import fuzz

class Reconcile(Document):
	def on_submit(self):
		fulldata = []
		for sl in self.slips:
			result1 = frappe.db.sql('''select sd.cheque_date as s_cd,sd.cheque_number as s_cn,sd.micr_code as s_micr,
								sd.short_code as s_san,sd.amount as s_amt,bd.cheque_date as b_cd,
								bd.cheque_no as b_cn,bd.micr as b_micr,bd.san as b_san,bd.amount as b_amt
								from `tabSlip Cheque Details` as sd inner join `tabStatement Details` as bd
								on sd.code = bd.code
								where sd.parent = "{0}" and bd.parent = "{1}"'''.format(sl.slip,self.bank_statement),as_dict = 1)
			if result1:					
				for row in result1:
					row['match_status'] = "Fully Match"
					row['not_matching_fields'] = ""		
					fulldata.append(row)

			result2 = frappe.db.sql('''select sd.cheque_date as s_cd,sd.cheque_number as s_cn,sd.micr_code as s_micr,
								sd.short_code as s_san,sd.amount as s_amt,bd.cheque_date as b_cd,
								bd.cheque_no as b_cn,bd.micr as b_micr,bd.san as b_san,bd.amount as b_amt
								from `tabSlip Cheque Details` as sd inner join `tabStatement Details` as bd
								on sd.amount_mis_code = bd.amount_mis_code
								where sd.code != bd.code and sd.micr_mis_code != bd.micr_mis_code and
								sd.cheque_no_mis_code != bd.cheque_no_mis_code and sd.san_miss_code != bd.san_mis_code and
								sd.parent = "{0}" and bd.parent = "{1}"'''.format(sl.slip,self.bank_statement),as_dict = 1)
			if result2:
				for row in result2:
					row['match_status'] = "Four Match"
					row['not_matching_fields'] = "Amount"
					fulldata.append(row)	

			result3 = frappe.db.sql('''select sd.cheque_date as s_cd,sd.cheque_number as s_cn,sd.micr_code as s_micr,
								sd.short_code as s_san,sd.amount as s_amt,bd.cheque_date as b_cd,
								bd.cheque_no as b_cn,bd.micr as b_micr,bd.san as b_san,bd.amount as b_amt 
								from `tabSlip Cheque Details` as sd inner join `tabStatement Details` as bd
								on sd.micr_mis_code = bd.micr_mis_code
								where sd.code != bd.code and sd.amount_mis_code != bd.amount_mis_code and
								sd.cheque_no_mis_code != bd.cheque_no_mis_code and sd.san_miss_code != bd.san_mis_code and
								sd.parent = "{0}" and bd.parent = "{1}"'''.format(sl.slip,self.bank_statement),as_dict = 1)
			if result3:
				for row in result3:
					row['match_status'] = "Four Match"
					row['not_matching_fields'] = "MICR"				
					fulldata.append(row)	

			result4 = frappe.db.sql('''select sd.cheque_date as s_cd,sd.cheque_number as s_cn,sd.micr_code as s_micr,
								sd.short_code as s_san,sd.amount as s_amt,bd.cheque_date as b_cd,
								bd.cheque_no as b_cn,bd.micr as b_micr,bd.san as b_san,bd.amount as b_amt
								from `tabSlip Cheque Details` as sd inner join `tabStatement Details` as bd
								on sd.cheque_no_mis_code = bd.cheque_no_mis_code
								where sd.code != bd.code and sd.amount_mis_code != bd.amount_mis_code and 
								sd.micr_mis_code != bd.micr_mis_code and sd.san_miss_code != bd.san_mis_code and
								sd.parent = "{0}" and bd.parent = "{1}"'''.format(sl.slip,self.bank_statement),as_dict = 1)
			if result4:
				for row in result4:
					row['match_status'] = "Four Match"
					row['not_matching_fields'] = "Cheque No"				
					fulldata.append(row)

			result5 = frappe.db.sql('''select sd.cheque_date as s_cd,sd.cheque_number as s_cn,sd.micr_code as s_micr,
								sd.short_code as s_san,sd.amount as s_amt,bd.cheque_date as b_cd,
								bd.cheque_no as b_cn,bd.micr as b_micr,bd.san as b_san,bd.amount as b_amt
								from `tabSlip Cheque Details` as sd inner join `tabStatement Details` as bd
								on sd.san_miss_code = bd.san_mis_code
								where sd.code != bd.code and sd.amount_mis_code != bd.amount_mis_code and 
								sd.micr_mis_code != bd.micr_mis_code and sd.cheque_no_mis_code != bd.cheque_no_mis_code and 
								sd.parent = "{0}" and bd.parent = "{1}"'''.format(sl.slip,self.bank_statement),as_dict = 1)
			if result5:
				for row in result5:
					row['match_status'] = "Four Match"
					row['not_matching_fields'] = "Short Code"					
					fulldata.append(row)

		if fulldata:
			rr = frappe.new_doc("Reconciled Results")
			rr.reconcile = self.name

			for i in fulldata:
				rrt_item = frappe.new_doc("Reconcile Details")
				rrt_item.s_cheque_no = i["s_cn"]
				rrt_item.s_cheque_date = i["s_cd"]
				rrt_item.s_micr_code = i["s_micr"]
				rrt_item.s_short_code = i["s_san"]
				rrt_item.s_amount = i["s_amt"]
				rrt_item.b_cheque_no = i["b_cn"]
				rrt_item.b_cheque_date = i["b_cd"]
				rrt_item.b_micr_code = i["b_micr"]
				rrt_item.b_short_code = i["b_san"]
				rrt_item.b_amount = i["b_amt"]
				rrt_item.match_status = i["match_status"]
				rrt_item.not_matching_fields = i["not_matching_fields"]
				rr.append("reconcile_one", rrt_item)

			rr.save()

		return fulldata

	def submit(self):
		if self.bank_statement:
			msgprint(_("The Reconcile task has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this Reconcile and revert to the Draft stage"))
			self.queue_action('submit', timeout=30000)
		else:
			self._submit()	


							

	# def on_submit(self):
	# 	slip_records = []
	# 	for sl in self.slips:
	# 		slip_record = frappe.db.sql('''select cheque_date,cheque_number,account_no,micr_code,short_code,amount,code from `tabSlip Cheque Details` 
	# 							where `tabSlip Cheque Details`.parent = "{0}"'''.format(sl.slip),as_dict = 1)
	# 		for slp in slip_record:					
	# 			slip_records.append(slp)					

	# 	if self.bank_statement:
	# 		bank_s_no = self.bank_statement
		
	# 	bank_record = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr,san,amount,code from `tabStatement Details` 
	# 							where `tabStatement Details`.parent = "{0}" '''.format(bank_s_no),as_dict = 1)

	# 	row_list = {}
	# 	# perc = []
	# 	fulldata = []
	# 	idx = 0

	# 	def reconcile_data():
	# 		match = 0
	# 		row_list['not_matching_fields'] = ""
	# 		row_list['values'] = ""
	# 		row_list['code'] = b.code
	# 		if b.cheque_no == s.cheque_number:
	# 			match +=1
	# 			row_list['cheque_no'] = b.cheque_no
	# 		else:
	# 			row_list['cheque_no'] = b.cheque_no
	# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
	# 			row_list['values'] = row_list['values'] + "," + s.cheque_number

	# 		if b.cheque_date == s.cheque_date:
	# 			match +=1
	# 			row_list['cheque_date'] = b.cheque_date
	# 		else:
	# 			row_list['cheque_date'] = b.cheque_date
	# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
	# 			row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

	# 		if b.micr == s.micr_code:
	# 			match +=1
	# 			row_list['micr_code'] = b.micr
	# 		else:
	# 			row_list['micr_code'] = b.micr
	# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
	# 			row_list['values'] = row_list['values'] + "," + s.micr_code

	# 		if b.san == s.short_code:
	# 			match += 1
	# 			row_list['short_code'] = b.san
	# 		else:
	# 			row_list['short_code'] = b.san
	# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
	# 			row_list['values'] = row_list['values'] + "," + s.short_code

	# 		if b.amount == s.amount:
	# 			match +=1
	# 			row_list['amount'] = b.amount
	# 		else:
	# 			row_list['amount'] = b.amount
	# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
	# 			row_list['values'] = row_list['values'] + "," + str(s.amount)
	# 		row_list['main_from'] = "Bank Statement"
	# 		row_list['checked_code'] = s.code

	# 		if match == 0:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "No Match"
	# 		elif match == 1:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "One Match"
	# 		elif match == 2:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "Two Match"
	# 		elif match == 3:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "Three Match"
	# 		elif match == 4:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "Four Match"
	# 		elif match == 5:
	# 			row_list['match'] = match
	# 			row_list['match_status'] = "Fully Match"

	# 		if idx == 0:
	# 			row_list_copy = row_list.copy()
	# 			fulldata.append(row_list_copy)
			
	# 		list_of_all_values = [value for elem in fulldata
	# 								for value in elem.values()]									
	# 		bank_code = row_list['code']
	# 		slip_code = row_list['checked_code']
	# 		if not bank_code in list_of_all_values and not slip_code in list_of_all_values:
	# 			row_list_copy = row_list.copy()
	# 			fulldata.append(row_list_copy)	


	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			# perc.append(per)
	# 			if per == 100:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 99:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 98:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 97:
	# 				reconcile_data()
	# 		idx +=1
		
	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 96:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 95:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 94:
	# 				reconcile_data()
	# 		idx +=1
			
	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 93:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 92:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 91:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 90:
	# 				reconcile_data()
	# 		idx +=1		

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 89:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 88:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 87:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 86:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 85:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 84:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 83:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 82:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 81:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 80:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 79:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 78:
	# 				reconcile_data()
	# 		idx +=1	
			
	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 77:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 76:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 75:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 74:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 73:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 72:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 71:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 70:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 69:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 68:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 67:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 66:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 65:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 64:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 63:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 62:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 61:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 60:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 59:
	# 				reconcile_data()
	# 		idx +=1

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 58:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 57:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 56:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 55:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 54:
	# 				reconcile_data()
	# 		idx +=1			

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 53:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 52:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 51:
	# 				reconcile_data()
	# 		idx +=1	

	# 	if len(fulldata) < 1:
	# 		idx = 0
		
	# 	for b in bank_record:
	# 		match = 0
	# 		for s in slip_records:
	# 			per = fuzz.ratio(b.code, s.code)
	# 			#perc.append(per)
	# 			if per == 50:
	# 				reconcile_data()
	# 		idx +=1
																														
	# 	for sp in slip_records:
	# 		list_of_all_values = [value for elem in fulldata
	# 								for value in elem.values()]
	# 		value = sp.code
	# 		if not value in list_of_all_values:
	# 			row_list['code'] = ""
	# 			row_list['checked_code'] = sp.code
	# 			row_list['cheque_no'] = sp.cheque_number
	# 			row_list['cheque_date'] = str(sp.cheque_date)
	# 			row_list['micr_code'] = sp.micr_code
	# 			row_list['short_code'] = sp.short_code
	# 			row_list['amount'] = str(sp.amount)
	# 			row_list['main_from'] = "Slip"
	# 			row_list['match'] = 0
	# 			row_list['match_status'] = "No Match for Bank Statement"
	# 			row_list['not_matching_fields'] = ""
	# 			row_list['values'] = ""

	# 			row_list_copy = row_list.copy()
	# 			fulldata.append(row_list_copy)

	# 	for br in bank_record:
	# 		list_of_all_values = [value for elem in fulldata
	# 								for value in elem.values()]
	# 		value = br.code
	# 		if not value in list_of_all_values:
	# 			row_list['code'] = br.code
	# 			row_list['checked_code'] = ""
	# 			row_list['cheque_no'] = br.cheque_no
	# 			row_list['cheque_date'] = str(br.cheque_date)
	# 			row_list['micr_code'] = br.micr
	# 			row_list['short_code'] = br.san
	# 			row_list['amount'] = str(br.amount)
	# 			row_list['main_from'] = "Bank Statement"
	# 			row_list['match'] = 0
	# 			row_list['match_status'] = "No Match for Slip line"
	# 			row_list['not_matching_fields'] = ""
	# 			row_list['values'] = ""

	# 			row_list_copy = row_list.copy()
	# 			fulldata.append(row_list_copy)		
							
	# 	if fulldata:
	# 		rr = frappe.new_doc("Reconciled Results")
	# 		rr.reconcile = self.name

	# 		for i in fulldata:
	# 			rrt_item = frappe.new_doc("Reconcile Details")
	# 			rrt_item.cheque_no = i["cheque_no"]
	# 			rrt_item.cheque_date = i["cheque_date"]
	# 			rrt_item.micr_code = i["micr_code"]
	# 			rrt_item.short_code = i["short_code"]
	# 			rrt_item.amount = i["amount"]
	# 			rrt_item.match_value = i["match"]
	# 			rrt_item.match_status = i["match_status"]
	# 			rrt_item.not_matching_fields = i["not_matching_fields"]
	# 			rrt_item.values = i["values"]
	# 			rrt_item.main_from = i["main_from"]
	# 			rrt_item.code = i["code"]
	# 			rrt_item.checked_code = i["checked_code"]
	# 			rr.append("reconcile_one", rrt_item)

	# 		rr.save()

	# 	return fulldata	
	

# @frappe.whitelist()
# def reconcile_fun(slips , bank_statement):
# 	slipss = json.loads(slips)
# 	slip_records = []
# 	for sl in slipss:
# 		slip_record = frappe.db.sql('''select cheque_date,cheque_number,account_no,micr_code,short_code,amount,code from `tabSlip Cheque Details` 
# 							where `tabSlip Cheque Details`.parent = "{0}"'''.format(sl),as_dict = 1)
# 		for slp in slip_record:					
# 			slip_records.append(slp)					

# 	if bank_statement:
# 		bank_s_no = bank_statement
	
# 	bank_record = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr,san,amount,code from `tabStatement Details` 
# 							where `tabStatement Details`.parent = "{0}" '''.format(bank_s_no),as_dict = 1)


# 	row_list = {}
# 	# perc = []
# 	fulldata = []
# 	idx = 0

# 	def reconcile_data():
# 		match = 0
# 		row_list['not_matching_fields'] = ""
# 		row_list['values'] = ""
# 		row_list['code'] = b.code
# 		if b.cheque_no == s.cheque_number:
# 			match +=1
# 			row_list['cheque_no'] = b.cheque_no
# 		else:
# 			row_list['cheque_no'] = b.cheque_no
# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
# 			row_list['values'] = row_list['values'] + "," + s.cheque_number

# 		if b.cheque_date == s.cheque_date:
# 			match +=1
# 			row_list['cheque_date'] = b.cheque_date
# 		else:
# 			row_list['cheque_date'] = b.cheque_date
# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
# 			row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

# 		if b.micr == s.micr_code:
# 			match +=1
# 			row_list['micr_code'] = b.micr
# 		else:
# 			row_list['micr_code'] = b.micr
# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
# 			row_list['values'] = row_list['values'] + "," + s.micr_code

# 		if b.san == s.short_code:
# 			match += 1
# 			row_list['short_code'] = b.san
# 		else:
# 			row_list['short_code'] = b.san
# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
# 			row_list['values'] = row_list['values'] + "," + s.short_code

# 		if b.amount == s.amount:
# 			match +=1
# 			row_list['amount'] = b.amount
# 		else:
# 			row_list['amount'] = b.amount
# 			row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
# 			row_list['values'] = row_list['values'] + "," + str(s.amount)
# 		row_list['main_from'] = "Bank Statement"
# 		row_list['checked_code'] = s.code

# 		if match == 0:
# 			row_list['match'] = match
# 			row_list['match_status'] = "No Match"
# 		elif match == 1:
# 			row_list['match'] = match
# 			row_list['match_status'] = "One Match"
# 		elif match == 2:
# 			row_list['match'] = match
# 			row_list['match_status'] = "Two Match"
# 		elif match == 3:
# 			row_list['match'] = match
# 			row_list['match_status'] = "Three Match"
# 		elif match == 4:
# 			row_list['match'] = match
# 			row_list['match_status'] = "Four Match"
# 		elif match == 5:
# 			row_list['match'] = match
# 			row_list['match_status'] = "Fully Match"

# 		if idx == 0:
# 			row_list_copy = row_list.copy()
# 			fulldata.append(row_list_copy)
		
# 		list_of_all_values = [value for elem in fulldata
# 								for value in elem.values()]									
# 		bank_code = row_list['code']
# 		slip_code = row_list['checked_code']
# 		if not bank_code in list_of_all_values and not slip_code in list_of_all_values:
# 			row_list_copy = row_list.copy()
# 			fulldata.append(row_list_copy)	


# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			# perc.append(per)
# 			if per == 100:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 99:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 98:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 97:
# 				reconcile_data()
# 		idx +=1
	
# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 96:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 95:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 94:
# 				reconcile_data()
# 		idx +=1
		
# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 93:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 92:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 91:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 90:
# 				reconcile_data()
# 		idx +=1		

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 89:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 88:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 87:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 86:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 85:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 84:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 83:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 82:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 81:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 80:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 79:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 78:
# 				reconcile_data()
# 		idx +=1	
		
# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 77:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 76:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 75:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 74:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 73:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 72:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 71:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 70:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 69:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 68:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 67:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 66:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 65:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 64:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 63:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 62:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 61:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 60:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 59:
# 				reconcile_data()
# 		idx +=1

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 58:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 57:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 56:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 55:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 54:
# 				reconcile_data()
# 		idx +=1			

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 53:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 52:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 51:
# 				reconcile_data()
# 		idx +=1	

# 	if len(fulldata) < 1:
# 		idx = 0
	
# 	for b in bank_record:
# 		match = 0
# 		for s in slip_records:
# 			per = fuzz.ratio(b.code, s.code)
# 			#perc.append(per)
# 			if per == 50:
# 				reconcile_data()
# 		idx +=1
																													
# 	for sp in slip_records:
# 		list_of_all_values = [value for elem in fulldata
# 								for value in elem.values()]
# 		value = sp.code
# 		if not value in list_of_all_values:
# 			row_list['code'] = ""
# 			row_list['checked_code'] = sp.code
# 			row_list['cheque_no'] = sp.cheque_number
# 			row_list['cheque_date'] = str(sp.cheque_date)
# 			row_list['micr_code'] = sp.micr_code
# 			row_list['short_code'] = sp.short_code
# 			row_list['amount'] = str(sp.amount)
# 			row_list['main_from'] = "Slip"
# 			row_list['match'] = 0
# 			row_list['match_status'] = "No Match for Bank Statement"
# 			row_list['not_matching_fields'] = ""
# 			row_list['values'] = ""

# 			row_list_copy = row_list.copy()
# 			fulldata.append(row_list_copy)

# 	for br in bank_record:
# 		list_of_all_values = [value for elem in fulldata
# 								for value in elem.values()]
# 		value = br.code
# 		if not value in list_of_all_values:
# 			row_list['code'] = br.code
# 			row_list['checked_code'] = ""
# 			row_list['cheque_no'] = br.cheque_no
# 			row_list['cheque_date'] = str(br.cheque_date)
# 			row_list['micr_code'] = br.micr
# 			row_list['short_code'] = br.san
# 			row_list['amount'] = str(br.amount)
# 			row_list['main_from'] = "Bank Statement"
# 			row_list['match'] = 0
# 			row_list['match_status'] = "No Match for Slip line"
# 			row_list['not_matching_fields'] = ""
# 			row_list['values'] = ""

# 			row_list_copy = row_list.copy()
# 			fulldata.append(row_list_copy)		
						

# 	return fulldata
