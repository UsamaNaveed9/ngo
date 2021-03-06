
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
	fulldata = []

	for b in bank_record:
		match = 0
		for s in slip_records:
			per = fuzz.ratio(b.code, s.code)
			if per > 95 :
				row_list['code'] = b.code
				if b.san == s.short_code:
					match += 1
					row_list['short_code'] = b.san
				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no	
				if b.account_no == s.account_no:
					match +=1
					row_list['account_no'] = b.account_no
				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr	
				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount

		if match > 0 and match < 6:
			row_list['match'] = match
			row_list['match_status'] = "Partially Match"
		elif match == 6:
			row_list['match'] = match
			row_list['match_status'] = "Fully Match"
		else:
			row_list['match'] = match
			row_list['match_status'] = "No Match"

		row_list_copy = row_list.copy()
		fulldata.append(row_list_copy)


	return fulldata