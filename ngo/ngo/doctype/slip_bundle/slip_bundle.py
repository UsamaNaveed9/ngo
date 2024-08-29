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