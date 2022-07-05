# -*- coding: utf-8 -*-
# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Reconcile(Document):
	pass

@frappe.whitelist()
def reconcile_fun(slip , bank_statement):
	if slip:
		slip_number = slip
	if bank_statement:
		bank_s_no = bank_statement
	slip_record = frappe.db.sql('''select cheque_date,cheque_number,account_no,micr_code,short_code,amount from `tabSlip Cheque Details` 
							where `tabSlip Cheque Details`.parent = "{0}"'''.format(slip_number),as_dict = 1)

	bank_record = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr,san,amount from `tabStatement Details` 
							where `tabStatement Details`.parent = "{0}" '''.format(bank_s_no),as_dict = 1)

	row_list = {}
	fulldata = []

	for b in bank_record:
		match = 0
		for s in slip_record:
			if b.san == s.short_code:
				match += 1
				row_list['short_code'] = b.san
				if b.cheque_date == s.cheque_date:
					match +=1
					row_list['cheque_date'] = b.cheque_date
				else:
					row_list['cheque_date'] = str(b.cheque_date) + " " + str(s.cheque_date)
				if b.cheque_no == s.cheque_number:
					match +=1
					row_list['cheque_no'] = b.cheque_no
				else:
					row_list['cheque_no'] = str(b.cheque_no) + " " + str(s.cheque_number)	
				if b.account_no == s.account_no:
					match +=1
					row_list['account_no'] = b.account_no
				else:
					row_list['account_no'] = str(b.account_no) + " " + str(s.account_no)	
				if b.micr == s.micr_code:
					match +=1
					row_list['micr_code'] = b.micr
				else:
					row_list['micr_code'] = str(b.micr) + " " + str(s.micr_code)	
				if b.amount == s.amount:
					match +=1
					row_list['amount'] = b.amount
				else:
					row_list['amount'] = str(b.amount) + " " + str(s.amount)

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