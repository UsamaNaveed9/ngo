# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ngo.ngo.doctype.slip_form.slip_form import validate_cheques
from ngo.ngo.report.duplicate_finder.duplicate_finder import execute as duplicate_finder_report

class SlipBundle(Document):
	def set_total_amount_and_total_cheques(self):
		self.slip_bundle_total_cheques = 0
		self.slip_bundle_total_amount = 0
		for item in self.items:
			self.slip_bundle_total_cheques += int(item.number_of_cheques)
			self.slip_bundle_total_amount += int(item.total_amount)
	
	def before_save(self):
		self.set_total_amount_and_total_cheques()

	def check_if_slip_forms_do_not_exist_in_another_bundle(self):
		for item in self.items:
			if not item.remarks:
				where_clauses = {"parent": ["!=", self.name], "slip_form": item.slip_form}
				findings = frappe.db.get_all("Slip Bundle Item", where_clauses, ["name", "parent", "slip_form"], group_by="parent")
				if len(findings) > 0:
					item.remarks = "Slip form found in {} bundles".format(', '.join([finding.parent for finding in findings]))
	
	def check_if_duplicate_account_or_duplicate_donor_exists_in_slip_forms(self):
		filter = {"slip_forms":[item.slip_form for item in self.items]}
		report_output = duplicate_finder_report(filter)

		if report_output[1]:
			for item in self.items:
				if not item.remarks:
					item.remarks = "Failing in Duplicate finder"
					

	def validate_slip_forms(self):
		for item in self.items:
			if not item.remarks:
				item.remarks = "{} errors in validation".format(str(len(validate_cheques(item.slip_form))))

@frappe.whitelist()
def validate_slip_bundle(slip_bundle_name):
	slip_bundle = frappe.get_doc("Slip Bundle", slip_bundle_name)

	slip_bundle.check_if_slip_forms_do_not_exist_in_another_bundle()
	slip_bundle.validate_slip_forms()
	slip_bundle.check_if_duplicate_account_or_duplicate_donor_exists_in_slip_forms()
	
	slip_bundle.save()

@frappe.whitelist()
def download_slip_bundle_summary(slip_bundle_name):
	slip_bundle = frappe.get_doc("Slip Bundle", slip_bundle_name)

	slip_bundle_summary_content = []
	# Date
	slip_bundle_summary_content.append(','.join(map(str, [slip_bundle.slip_bundle_date])))
	# Address
	slip_bundle_summary_content.append(','.join(map(str, [slip_bundle.deposit_account])))
	# Slip Form Header
	header = ['Sr.no', 'Slip Number', 'Sum of Amount', 'Count of Cheques']
	slip_bundle_summary_content.append(','.join(map(str, header)))
	# Entries
	for i in slip_bundle.items:
		tmp = [
			i.idx,
			i.slip_form,
			i.total_amount,
			i.number_of_cheques
		]
		slip_bundle_summary_content.append(','.join(map(str, tmp)))
	# Total
	total = ['', 'Total', slip_bundle.slip_bundle_total_amount, slip_bundle.slip_bundle_total_cheques]
	slip_bundle_summary_content.append(','.join(map(str, total)))

	frappe.response.filename = "{}-summary.csv".format(slip_bundle_name)
	frappe.response.filecontent = '\n'.join(slip_bundle_summary_content)
	frappe.response.type = "download"
	frappe.response.display_content_as = "attachment"
	return

@frappe.whitelist()
def download_slip_bundle_details(slip_bundle_name):
	slip_bundle = frappe.get_doc("Slip Bundle", slip_bundle_name)

	slip_bundle_details_content = []
	# Date
	slip_bundle_details_content.append(','.join(map(str, [slip_bundle.slip_bundle_date])))
	# Address
	slip_bundle_details_content.append(','.join(map(str, [slip_bundle.deposit_account])))
	# Slip Form Header
	header = ['Sr. No.', 'Slip Number', 'SrNo', 'Account No', 'Cheque Bank', 'Cheque Number', 'Short Code', 'MICR Code']
	slip_bundle_details_content.append(','.join(map(str, header)))
	# Entries
	curr_no = 1
	for i in slip_bundle.items:
		slip_form = frappe.get_doc("Slip Form", i.slip_form)

		for j in slip_form.cheque_details:
			tmp = [
				curr_no,
				slip_form.name,
				j.srno,
				j.account_no,
				j.cheque_bank,
				j.cheque_number,
				j.short_code,
				j.micr_code
			]
			slip_bundle_details_content.append(','.join(map(str, tmp)))
			curr_no += 1

	frappe.response.filename = "{}-details.csv".format(slip_bundle_name)
	frappe.response.filecontent = '\n'.join(slip_bundle_details_content)
	frappe.response.type = "download"
	frappe.response.display_content_as = "attachment"
	return