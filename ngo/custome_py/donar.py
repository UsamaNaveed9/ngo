import frappe
@frappe.whitelist()

def get_data_from_bank_donar_details(donar_id,account_number):
	
	bank_donar_details = frappe.db.get_list("Bank Account",{"donor_id":donar_id,"name":account_number},["micr","short_account_number","branch_code","bank"])
	
	return bank_donar_details