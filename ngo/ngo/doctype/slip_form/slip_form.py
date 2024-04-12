# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SlipForm(Document):
	pass





@frappe.whitelist()
def get_donor_details_from_account(account_no):
	account_details = frappe.db.get_all("Bank Account",{"account_name":account_no},["account_name","donor_id"])
	if account_details:
		if account_details[0].get("donor_id"):
			donor_data = frappe.db.get_all("Donor",{"name":account_details[0].get("donor_id")},["donor_name","middle_name","last_name","name"])
			for donor in donor_data:
				full_name_parts = [donor.get('donor_name', ''), donor.get('middle_name', ''), donor.get('last_name', '')]
				full_name = ' '.join(part if part else ' ' for part in full_name_parts).strip()
				donor["full_name"] = full_name

				

				return donor 


@frappe.whitelist()
def get_donor_details_from_donar_id(donor_id_number):
	if donor_id_number:
		donor_data = frappe.db.get_all("Donor",{"name":donor_id_number},["donor_name","middle_name","last_name","name"])
		for donor in donor_data:
			full_name_parts = [donor.get('donor_name', ''), donor.get('middle_name', ''), donor.get('last_name', '')]
			full_name = ' '.join(part if part else ' ' for part in full_name_parts).strip()
			donor["full_name"] = full_name
			bank_details = frappe.db.get_all("Bank Account",{"donor_id":donor["name"]},["account_name","donor_id"])
			donor["account_name"]  =  bank_details[0].get("account_name")

			
			return donor 



