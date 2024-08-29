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

@frappe.whitelist()
def validate_cheques(slip_form_name):
	errors = []
	slip_form = frappe.get_doc("Slip Form", slip_form_name)

	for cheque in slip_form.cheque_details:
		error = {}
		print(cheque)
		print()

		if not cheque.amount: 
			error['Amount'] = "Amount is 0"
		if not (len(cheque.short_code or '')) == 6 and (cheque.short_code or '').isdigit():
			error['Short Code'] = "Short code is not 6 digit number"
		if not (len(cheque.micr_code or '')) == 9 and (cheque.micr_code or '').isdigit():
			error['MICR'] = "MICR is not 9 digit number"
		if not (len(cheque.cheque_number or '')) == 6 and (cheque.cheque_number or '').isdigit():
			error['Cheque Number'] = "Cheque Number is not 6 digit number"
		if not cheque.account_no:
			error['Account Number'] = "Account Number is not set"
		else:
			repeated_account_number = []
			for x in slip_form.cheque_details:
				if (x.account_no or '') == cheque.account_no:
					repeated_account_number.append(x)
			if len(repeated_account_number) > 1:
				error['Account Number'] = "Account Number repeated at " + ', '.join([str(x.srno) for x in repeated_account_number])
		if not cheque.donor_id_number:
			error['Donor Id'] = "Donor Id is not set"
		else:
			repeated_donor_id = []
			for x in slip_form.cheque_details:
				if (x.donor_id_number or '') == cheque.donor_id_number:
					repeated_donor_id.append(x)
			if len(repeated_donor_id) > 1:
				error['Donor Id'] = "Donor Id repeated at " + ', '.join([str(x.srno) for x in repeated_donor_id])
		if len(list(error.keys())) > 0:
			error['Id'] = cheque.idx
			errors.append(error)

	return errors

@frappe.whitelist()
def set_donor_from_account(slip_form_name):
	slip_form = frappe.get_doc("Slip Form", slip_form_name)

	for cheque in slip_form.cheque_details:
		if cheque.account_no:
			donor_id = frappe.db.get_value("Bank Account", cheque.account_no, "donor_id")
			if donor_id:
				donor = frappe.get_doc("Donor", donor_id)
				full_name = []
				if donor.donor_name:
					full_name.append(donor.donor_name)
				if donor.middle_name:
					full_name.append(donor.middle_name)
				if donor.last_name:
					full_name.append(donor.last_name)
				
				cheque.donor_id_number = donor_id
				cheque.donor_name = ' '.join(full_name)
	
	slip_form.save()

@frappe.whitelist()
def return_cheques_and_block_donors(slip_form_name):
	if slip_form_name.startswith("RC"):
		slip_form = frappe.get_doc("Slip Form", slip_form_name)

		for cheque in slip_form.cheque_details:
			filters = {
				'amount': cheque.amount,
				'account_no': cheque.account_no,
				'unique_row_identifier': cheque.unique_row_identifier,
			}
			og_cheque_list = frappe.db.get_all("Slip Cheque Form", filters)

			if len(og_cheque_list) == 1:
				og_cheque_name = og_cheque_list[0]['name']

				frappe.db.set_value("Slip Cheque Form", og_cheque_name, "clearing_status", "RETURNED")
				frappe.db.set_value("Slip Cheque Form", og_cheque_name, "ref_link", slip_form_name)
				frappe.db.set_value("Slip Cheque Form", og_cheque_name, "ref_id_sr_number", cheque.srno)

				og_cheque = frappe.get_doc("Slip Cheque Form", og_cheque_name)
				cheque.ref_link = og_cheque.parent
				cheque.ref_id_sr_number = og_cheque.srno

			if slip_form_name.startswith("RC-NB"):
				if cheque.donor_id_number:
					donor = frappe.get_doc("Donor", cheque.donor_id_number)

					donor.blocked_status = "BLOCKED"
					remarks1_new = "Blocked for {}, {}".format(cheque.ref_link, cheque.ref_id_sr_number)
					remarks1 = [] if donor.remarks1 in [None, ""] else donor.get("remarks1", "").split("\n")
					remarks1.append(remarks1_new)
					donor.remarks1 = "\n".join(remarks1)
					donor.save()

		slip_form.save()