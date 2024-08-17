# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt

import frappe
import pandas as pd


def execute(filters=None):
	columns = [
		{
			'fieldname': 'donor_id_number',
			'label': frappe._('Donor Id'),
			'fieldtype': 'Link',
			'options': 'Donor'
		},
		{
			'fieldname': 'donor_id_number_count',
			'label': frappe._('Donor Id Count'),
			'fieldtype': 'Int'
		},
		{
			'fieldname': 'account_no',
			'label': frappe._('Bank Account'),
			'fieldtype': 'Link',
			'options': 'Bank Account'
		},
		{
			'fieldname': 'account_no_count',
			'label': frappe._('Bank Account Count'),
			'fieldtype': 'Int'
		},
		{
			'fieldname': 'parent',
			'label': frappe._('Slip Form'),
			'fieldtype': 'Link',
			'options': 'Slip Form'
		},
		{
			'fieldname': 'srno',
			'label': frappe._('Cheque Serial Number'),
			'fieldtype': 'Int'
		}
	]
	data = []

	print(filters, 'filters')

	slip_forms = []
	query_filters = {}
	if 'event' in filters:
		slip_forms = [i.name for i in frappe.db.get_list('Slip Form', filters={'slip_event_code': filters['event']})]
	
	if len(filters['slip_forms']) > 0:
		slip_forms = filters['slip_forms']

	if len(slip_forms) > 0:
		query_filters['parent'] = ['IN', slip_forms]

	data_ = frappe.db.get_list('Slip Cheque Form', fields=['donor_id_number', 'account_no', 'parent', 'srno'], page_length=100000, filters=query_filters, debug=True)
	print(data_, 'data_', len(data_))
	
	df = pd.DataFrame.from_records(data_)
	df['donor_id_number_count'] = df.groupby(['donor_id_number'])['donor_id_number'].transform('count')
	df['account_no_count'] = df.groupby(['account_no'])['account_no'].transform('count')
	data = df.loc[(df['donor_id_number_count'] > 1) | (df['account_no_count'] > 1)].to_dict('records')

	
	return columns, data
