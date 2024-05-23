# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SlipForm(Document):
	def create_deleted_record(self):
		# Extract the numerical part from the existing slip number
		try:
			numeric_suffix = int(''.join(filter(str.isdigit, self.slip_number.split('-')[-1])))
		except ValueError:
			numeric_suffix = 0

		# Function to generate the next unique slip number
		def generate_unique_slip_number(base_number, current_suffix):
			while True:
				incremented_suffix = current_suffix + 1
				new_slip_number = f"DT - {base_number} - {incremented_suffix}"
				if not frappe.db.exists("Slip Form", {"slip_number": new_slip_number}):
					return new_slip_number, incremented_suffix
				current_suffix = incremented_suffix

		# Generate the new unique slip number
		new_slip_number, incremented_numerical_suffix = generate_unique_slip_number(self.slip_number, numeric_suffix)

		# Create a new slip form document
		new_doc = frappe.new_doc("Slip Form")
		# Copy fields from the current document to the new document
		new_doc.update({
			'slip_date': self.slip_date,
			'slip_number': new_slip_number,
			'deposit_account': self.deposit_account,
			'deposit_bank': self.deposit_bank,
			'slip_event_code': self.slip_event_code,
			'lcd_form_pdf_name': self.lcd_form_pdf_name,
			'lcd_form_pdf_path': self.lcd_form_pdf_path,
			'internal_slip_number': self.internal_slip_number,
			'slip_event_description': self.slip_event_description,
			'slip_remark': self.slip_remark,
			'slip_receipt_print_status': self.slip_receipt_print_status,
			'slip_deposited_status': self.slip_deposited_status,
			'number_of_cheques_returned_or_rejected_in_slip': self.number_of_cheques_returned_or_rejected_in_slip,
			'attachments_which_are_connected_to_the_slip': self.attachments_which_are_connected_to_the_slip,
			'number_of_cheques_in_slip': self.number_of_cheques_in_slip,
			'number_of_cheques_deposited_in_slip': self.number_of_cheques_deposited_in_slip,
			'total_amount_of_deposited_cheques': self.total_amount_of_deposited_cheques,
			'total_amount_in_slip': self.total_amount_in_slip
		})

		cheques_to_remove = []

		# Iterate over the cheques and separate the blocked ones
		for cheque in self.cheque_details:
			if cheque.is_block or cheque.donor_status == "Blocked":
				new_cheque = frappe.new_doc("Slip Cheque Form")
				new_cheque.update({
					'amount': cheque.amount,
					'donor_id_number': cheque.donor_id_number,
					'account_no': cheque.account_no,
					'donor_name': cheque.donor_name,
					'check_image': cheque.check_image,
					'missing_check_details': cheque.missing_check_details,
					'token': cheque.token,
					'srno': cheque.srno,
					'cheque_bank': cheque.cheque_bank,
					'cheque_date': cheque.cheque_date,
					'cheque_number': cheque.cheque_number,
					'micr_code': cheque.micr_code,
					'short_code': cheque.short_code,
					'donor_status': cheque.donor_status,
					'is_block': cheque.is_block,
					'branch_code': cheque.branch_code,
					'clearing_status': cheque.clearing_status,
					'event_type': cheque.event_type,
					'ref_link': cheque.ref_link,
					'ref_id_sr_number': cheque.ref_id_sr_number,
					'code': cheque.code,
					'slip_item_system_recon_status': cheque.slip_item_system_recon_status,
					'slip_item_manual_recon_status': cheque.slip_item_manual_recon_status,
					'slip_item_uploaded_account_number': cheque.slip_item_uploaded_account_number,
					'attachments_available': cheque.attachments_available,
					'amount_mis_code': cheque.amount_mis_code,
					'event': cheque.event,
					'micr_mis_code': cheque.micr_mis_code,
					'cheque_no_mis_code': cheque.cheque_no_mis_code,
					'san_miss_code': cheque.san_miss_code,
					'cheque_image_file_name': cheque.cheque_image_file_name,
					'image': cheque.image,
					'slip_number': cheque.slip_number,
					'unique_row_identifier': cheque.unique_row_identifier    
				})
				new_doc.append("cheque_details", new_cheque)
				cheques_to_remove.append(cheque)

		# Remove blocked cheques from the original slip and adjust indices
		self.cheque_details = [cheque for cheque in self.cheque_details if cheque not in cheques_to_remove]
		total_amount = sum(cheque.amount for cheque in self.cheque_details)
		number_of_cheques = len(self.cheque_details)
		self.total_amount_in_slip = total_amount
		self.number_of_cheques_in_slip = number_of_cheques

		# Recalculate and update indices
		for idx, cheque in enumerate(self.cheque_details):
			cheque.idx = idx + 1

		# Save the new document and update the original document
		new_doc.save()
		self.save()
		frappe.db.commit()

		return new_doc.name



@frappe.whitelist()
def create_deleted_record(docname):
    doc = frappe.get_doc("Slip Form", docname)
    return doc.create_deleted_record()





@frappe.whitelist()
def get_donor_details_from_account(account_no):
	account_details = frappe.db.get_all("Bank Account",{"name":account_no},["account_name","donor_id","bank"])
	if account_details:
		if account_details[0].get("donor_id"):
			donor_data = frappe.db.get_all("Donor",{"name":account_details[0].get("donor_id")},["donor_name","middle_name","last_name","name","block_status"])
			for donor in donor_data:
				#status = donor.get('block_status')
				full_name_parts = [donor.get('donor_name', ''), donor.get('middle_name', ''), donor.get('last_name', '')]
				full_name = ' '.join(part if part else ' ' for part in full_name_parts).strip()
				donor["full_name"] = full_name
				donor["bank"] = account_details[0].get("bank")
				return donor 


@frappe.whitelist()
def get_donor_details_from_donar_id(donor_id_number):
	if donor_id_number:
		donor_data = frappe.db.get_all("Donor",{"name":donor_id_number},["donor_name","middle_name","last_name","name","block_status"])
		for donor in donor_data:
			full_name_parts = [donor.get('donor_name', ''), donor.get('middle_name', ''), donor.get('last_name', '')]
			full_name = ' '.join(part if part else ' ' for part in full_name_parts).strip()
			donor["full_name"] = full_name
			bank_details = frappe.db.get_all("Bank Account",{"donor_id":donor["name"]},["account_name","donor_id"])
			donor["account_name"]  =  bank_details[0].get("account_name")

			
			return donor 



