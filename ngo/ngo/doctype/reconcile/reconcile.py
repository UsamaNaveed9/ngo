
# -*- coding: utf-8 -*-
# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from fuzzywuzzy import fuzz

class Reconcile(Document):
	pass

@frappe.whitelist()
def reconcile_fun(slips , bank_statement):
	slipss = json.loads(slips)
	slip_records = []
	for sl in slipss:
		slip_record = frappe.db.sql('''select cheque_date,cheque_number,account_no,micr_code,short_code,amount,code from `tabSlip Cheque Details` 
							where `tabSlip Cheque Details`.parent = "{0}"'''.format(sl),as_dict = 1)
		for slp in slip_record:					
			slip_records.append(slp)					

	if bank_statement:
		bank_s_no = bank_statement
	
	bank_record = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr,san,amount,code from `tabStatement Details` 
							where `tabStatement Details`.parent = "{0}" '''.format(bank_s_no),as_dict = 1)


	row_list = {}
	# perc = []
	fulldata = []
	idx = 0
	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			#perc.append(per)
			if per > 98:
				match = 0
				row_list['not_matching_fields'] = ""
				row_list['values'] = ""
				row_list['code'] = b.code
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = b.cheque_no
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
					row_list['values'] = row_list['values'] + "," + s.cheque_number

				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = b.cheque_date
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
					row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = b.micr
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
					row_list['values'] = row_list['values'] + "," + s.micr_code

				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				else:
					row_list['short_code'] = b.san
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
					row_list['values'] = row_list['values'] + "," + s.short_code

				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = b.amount
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
					row_list['values'] = row_list['values'] + "," + str(s.amount)
				row_list['main_from'] = "Bank Statement"
				row_list['checked_code'] = s.code

				if match == 0:
					row_list['match'] = match
					row_list['match_status'] = "No Match"
					row_list['checked_code'] = ""
				elif match == 1:
					row_list['match'] = match
					row_list['match_status'] = "One Match"
				elif match == 2:
					row_list['match'] = match
					row_list['match_status'] = "Two Match"
				elif match == 3:
					row_list['match'] = match
					row_list['match_status'] = "Three Match"
				elif match == 4:
					row_list['match'] = match
					row_list['match_status'] = "Four Match"
				elif match == 5:
					row_list['match'] = match
					row_list['match_status'] = "Fully Match"

				if idx == 0:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)
		
				list_of_all_values = [value for elem in fulldata
								for value in elem.values()]									
				value = row_list['code']
				if not value in list_of_all_values:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)

		idx +=1


	if len(fulldata) < 1:
		idx = 0
	
	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			#perc.append(per)
			if per > 95:
				match = 0
				row_list['not_matching_fields'] = ""
				row_list['values'] = ""
				row_list['code'] = b.code
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = b.cheque_no
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
					row_list['values'] = row_list['values'] + "," + s.cheque_number

				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = b.cheque_date
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
					row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = b.micr
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
					row_list['values'] = row_list['values'] + "," + s.micr_code

				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				else:
					row_list['short_code'] = b.san
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
					row_list['values'] = row_list['values'] + "," + s.short_code

				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = b.amount
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
					row_list['values'] = row_list['values'] + "," + str(s.amount)
				row_list['main_from'] = "Bank Statement"
				row_list['checked_code'] = s.code				

				if match == 0:
					row_list['match'] = match
					row_list['match_status'] = "No Match"
					row_list['checked_code'] = ""
				elif match == 1:
					row_list['match'] = match
					row_list['match_status'] = "One Match"
				elif match == 2:
					row_list['match'] = match
					row_list['match_status'] = "Two Match"
				elif match == 3:
					row_list['match'] = match
					row_list['match_status'] = "Three Match"
				elif match == 4:
					row_list['match'] = match
					row_list['match_status'] = "Four Match"
				elif match == 5:
					row_list['match'] = match
					row_list['match_status'] = "Fully Match"

				if idx == 0:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)
		
				list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
				value = row_list['code']
				if not value in list_of_all_values:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)

		idx +=1

	if len(fulldata) < 1:
		idx = 0
	
	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			#perc.append(per)
			if per > 90:
				match = 0
				row_list['not_matching_fields'] = ""
				row_list['values'] = ""
				row_list['code'] = b.code
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = b.cheque_no
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
					row_list['values'] = row_list['values'] + "," + s.cheque_number

				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = b.cheque_date
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
					row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = b.micr
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
					row_list['values'] = row_list['values'] + "," + s.micr_code

				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				else:
					row_list['short_code'] = b.san
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
					row_list['values'] = row_list['values'] + "," + s.short_code

				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = b.amount
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
					row_list['values'] = row_list['values'] + "," + str(s.amount)
				row_list['main_from'] = "Bank Statement"
				row_list['checked_code'] = s.code				

				if match == 0:
					row_list['match'] = match
					row_list['match_status'] = "No Match"
					row_list['checked_code'] = ""
				elif match == 1:
					row_list['match'] = match
					row_list['match_status'] = "One Match"
				elif match == 2:
					row_list['match'] = match
					row_list['match_status'] = "Two Match"
				elif match == 3:
					row_list['match'] = match
					row_list['match_status'] = "Three Match"
				elif match == 4:
					row_list['match'] = match
					row_list['match_status'] = "Four Match"
				elif match == 5:
					row_list['match'] = match
					row_list['match_status'] = "Fully Match"

				if idx == 0:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)
		
				list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
				value = row_list['code']
				if not value in list_of_all_values:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)

		idx +=1

	if len(fulldata) < 1:
		idx = 0
	
	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			#perc.append(per)
			if per > 85:
				match = 0
				row_list['not_matching_fields'] = ""
				row_list['values'] = ""
				row_list['code'] = b.code
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = b.cheque_no
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
					row_list['values'] = row_list['values'] + "," + s.cheque_number

				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = b.cheque_date
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
					row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = b.micr
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
					row_list['values'] = row_list['values'] + "," + s.micr_code

				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				else:
					row_list['short_code'] = b.san
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
					row_list['values'] = row_list['values'] + "," + s.short_code

				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = b.amount
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
					row_list['values'] = row_list['values'] + "," + str(s.amount)
				row_list['main_from'] = "Bank Statement"
				row_list['checked_code'] = s.code			

				if match == 0:
					row_list['match'] = match
					row_list['match_status'] = "No Match"
					row_list['checked_code'] = ""
				elif match == 1:
					row_list['match'] = match
					row_list['match_status'] = "One Match"
				elif match == 2:
					row_list['match'] = match
					row_list['match_status'] = "Two Match"
				elif match == 3:
					row_list['match'] = match
					row_list['match_status'] = "Three Match"
				elif match == 4:
					row_list['match'] = match
					row_list['match_status'] = "Four Match"
				elif match == 5:
					row_list['match'] = match
					row_list['match_status'] = "Fully Match"

				if idx == 0:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)
		
				list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
				value = row_list['code']
				if not value in list_of_all_values:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)

		idx +=1
	
	if len(fulldata) < 1:
		idx = 0
	
	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			#perc.append(per)
			if per > 80:
				match = 0
				row_list['not_matching_fields'] = ""
				row_list['values'] = ""
				row_list['code'] = b.code
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = b.cheque_no
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque No"
					row_list['values'] = row_list['values'] + "," + s.cheque_number

				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = b.cheque_date
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Cheque Date"
					row_list['values'] = row_list['values'] + "," + str(s.cheque_date)

				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = b.micr
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "MICR Code"
					row_list['values'] = row_list['values'] + "," + s.micr_code

				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				else:
					row_list['short_code'] = b.san
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Short Code"
					row_list['values'] = row_list['values'] + "," + s.short_code

				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = b.amount
					row_list['not_matching_fields'] = row_list['not_matching_fields'] + "," + "Amount"
					row_list['values'] = row_list['values'] + "," + str(s.amount)
				row_list['main_from'] = "Bank Statement"
				row_list['checked_code'] = s.code			

				if match == 0:
					row_list['match'] = match
					row_list['match_status'] = "No Match"
					row_list['checked_code'] = ""
				elif match == 1:
					row_list['match'] = match
					row_list['match_status'] = "One Match"
				elif match == 2:
					row_list['match'] = match
					row_list['match_status'] = "Two Match"
				elif match == 3:
					row_list['match'] = match
					row_list['match_status'] = "Three Match"
				elif match == 4:
					row_list['match'] = match
					row_list['match_status'] = "Four Match"
				elif match == 5:
					row_list['match'] = match
					row_list['match_status'] = "Fully Match"

				if idx == 0:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)
		
				list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
				value = row_list['code']
				if not value in list_of_all_values:
					row_list_copy = row_list.copy()
					fulldata.append(row_list_copy)

		idx +=1

	for sp in slip_records:
		list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
		value = sp.code
		if not value in list_of_all_values:
			row_list['code'] = sp.code
			row_list['cheque_no'] = sp.cheque_number
			row_list['cheque_date'] = str(sp.cheque_date)
			row_list['micr_code'] = sp.micr_code
			row_list['short_code'] = sp.short_code
			row_list['amount'] = str(sp.amount)
			row_list['main_from'] = "Slip"
			row_list['match'] = 0
			row_list['match_status'] = "Not In Bank Statement"
			row_list['not_matching_fields'] = ""
			row_list['values'] = ""

			row_list_copy = row_list.copy()
			fulldata.append(row_list_copy)

	for br in bank_record:
		list_of_all_values = [value for elem in fulldata
								for value in elem.values()]
		value = br.code
		if not value in list_of_all_values:
			row_list['code'] = br.code
			row_list['cheque_no'] = br.cheque_no
			row_list['cheque_date'] = str(br.cheque_date)
			row_list['micr_code'] = br.micr
			row_list['short_code'] = br.san
			row_list['amount'] = str(br.amount)
			row_list['main_from'] = "Bank Statement"
			row_list['match'] = 0
			row_list['match_status'] = "Not In Slip"
			row_list['not_matching_fields'] = ""
			row_list['values'] = ""

			row_list_copy = row_list.copy()
			fulldata.append(row_list_copy)		
						

	return fulldata
