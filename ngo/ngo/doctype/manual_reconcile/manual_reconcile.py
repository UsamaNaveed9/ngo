# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class ManualReconcile(Document):
	pass

@frappe.whitelist()
def reconcile_fun(rec, status):
	rec_name = rec
	status = status
	rec_record = frappe.db.sql('''select code from `tabReconcile Details` 
	where `tabReconcile Details`.parent = "{0}" and `tabReconcile Details`.match_status = "{1}"'''.format(rec_name,status),as_dict = 1)

	return rec_record

@frappe.whitelist()
def reconcile_funAll(rec):
	rec_name = rec
	rec_record = frappe.db.sql('''select code from `tabReconcile Details` 
	where `tabReconcile Details`.parent = "{0}" '''.format(rec_name),as_dict = 1)

	return rec_record

@frappe.whitelist()
def get_slip_record(slips, code):
	slipss = json.loads(slips)
	slip_records = []
	for sl in slipss:
		slip_record = frappe.db.sql('''select cheque_date,cheque_number,account_no,micr_code,short_code,amount from `tabSlip Cheque Details` 
							where `tabSlip Cheque Details`.parent = "{0}" and `tabSlip Cheque Details`.code = "{1}"'''.format(sl,code),as_dict = 1)
		if slip_record:					
			slip_records.append(slip_record)

	return slip_record	

@frappe.whitelist()
def get_bs_record(bs_name, code):
	bs_row = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr,san,amount from `tabStatement Details` 
	where `tabStatement Details`.parent = "{0}" and `tabStatement Details`.code = "{1}"'''.format(bs_name,code),as_dict = 1)

	return bs_row

@frappe.whitelist()
def get_re_record(re_name,code):
	re_row = frappe.db.sql('''select cheque_date,cheque_no,account_no,micr_code,short_code,amount,match_value,match_status from `tabReconcile Details` 
	where `tabReconcile Details`.parent = "{0}" and `tabReconcile Details`.code = "{1}"'''.format(re_name,code),as_dict = 1)

	return re_row