# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt
import pandas as pd
import re
import frappe
from frappe.model.document import Document
from datetime import datetime
import os
import requests

from itertools import groupby
from operator import itemgetter
import json


class SlipScannerFilePath(Document):
	def autoname(self):
		now = datetime.now()
		custom_name = now.strftime("%d:%m:%y:%H:%M")
		self.name = custom_name 
	


def read_csv_(dict_list,df):
		
		filter_dict = []
		slip_number_lst = []
		missing_check_details = []
		
		for row in dict_list:
			date_of_slip = row.get("A")  # Extract date_of_slip from dictionary
			number = row.get("B")  # Extract number from dictionary

			check_number_ = row.get("B")
			event_master = row.get("event_master")

			filename = check_number_.split('\\')[-1]

			new_file_name = "/files/" + filename


			slip_number = None  # Initialize slip_number to None
			#event_code = None
			pattern = r'\\([^\\$]+)\$'
			number_ = re.findall(pattern, number)
			
			if number_:
				slip_number = number_[0]
				slip_number_lst.append(slip_number)
			bank_details = row.get("C")

			if isinstance(bank_details,str):
				bank_details = bank_details.replace('@', '')
				bank_details_str = bank_details.split("<")
				bank_details_str = [r for r in bank_details_str if r]
				
				if len(bank_details_str) > 0:
					bank_str = " ".join(bank_details_str)
					bank_str = bank_str.split(":")
					bank_str = " ".join(bank_str)
					bank_str = bank_str.split(" ")
					if len(bank_str) == 4:
						# Extract check_number, micr_code, short_account_number, and branch_code
						check_number = bank_str[0]
						micr_code = bank_str[1]
						short_account_number = bank_str[2]
						branch_code = bank_str[3]
						# Append extracted information to filter_dict
						filter_dict.append({
							"date_of_slip": date_of_slip,
							"slip_number": slip_number,
							"check_number": check_number,
							"micr_code": micr_code,
							"short_account_number": short_account_number,
							"branch_code": branch_code,
							"check_path_number":new_file_name,
							"bank_accounts":row.get("bank_accounts"),
							"account_name":row.get("account_name"),
							"slip_date":row.get("slip_date"),
							"event_master":row.get("event_master")
						})
					else:
						filter_dict.append({
							"date_of_slip": date_of_slip,
							"slip_number": slip_number,
							"missing_check_":number,
							"check_path_number":new_file_name,
							"bank_accounts":row.get("bank_accounts"),
							"account_name":row.get("account_name"),
							"slip_date":row.get("slip_date"),
							"event_master":row.get("event_master")

						})
						missing_check_details.append(number)
						


		
		list_of_check_number = []
		for row in filter_dict:
			list_of_check_number.append(row.get("check_path_number"))
		
		df = df[["A","B"]]
		dict_list_for_records_map = df.to_dict('records')

		for row in dict_list_for_records_map:
			check_number_ = row.get("B")
			filename = check_number_.split('\\')[-1]
			new_file_name = "/files/" + filename
			row["B"] = new_file_name


		pattern = r'\\([^\\$]+)\$'
		for row in dict_list_for_records_map:
			if row.get("B") not in list_of_check_number:
				match1 = re.search(pattern, row['B'])
				extracted_substring1 = match1.group(1) if match1 else None
				row["slip_number"] = extracted_substring1 
				row["date_of_slip"] = row.get("A")
				row["missing_check_"] = row.get("B")
				row.pop("A")
				row.pop("B")
				filter_dict.append(row)
		
		unique_account_number_lst = []
		frappe.errprint(unique_account_number_lst)
		unique_code_list_for_row = []
		# frappe.errprint(unique_code_list_for_row)
		for row in filter_dict:
			micr_code = row.get("micr_code")
			short_account_number = row.get("short_account_number")
			branch_code = row.get("branch_code")
			check_number = row.get("check_number")
			bank_account_details = frappe.db.get_all("Bank Account",
                                            filters={"micr": micr_code,
                                                    "short_account_number": short_account_number},
                                            fields=["name","donor_id","bank"])
			frappe.errprint(bank_account_details)
			if len(bank_account_details) == 1:
				# Check if donor_id exists in the bank account details
				if "donor_id" in bank_account_details[0]:
					row["account_no"] = bank_account_details[0]["name"]
					donor = bank_account_details[0]["donor_id"]
					row["cheque_bank"] = bank_account_details[0]["bank"]
					# Fetch the full name of the donor using the donor_id
					donor_name = frappe.get_value("Donor", donor, "donor_name")
					donor_status = frappe.get_value("Donor", donor, "block_status")
					if donor_name:
						row["donor"] = donor
						row["donor_name"] = donor_name
						row["donor_status"] = donor_status
					else:
						row["donor_name"] = None
				else:
					# Handle this case accordingly, e.g., set donor_id to None or skip this row
					row["account_no"] = bank_account_details[0]["name"]
					row["bank"] = bank_account_details[0]["bank"]
					row["donor"] = None
					row["donor_name"] = None
        
			# if bank_account_details:
			# 	row["account_no"] = bank_account_details[0]["name"]
			# 	row["donor"] = bank_account_details[0]["donor_id"]
			frappe.errprint(row)
			if micr_code:
				micr_code = add_zeroes_for_micr_code(micr_code)

			if short_account_number:
				short_account_number = add_zeroes_for_short_account_number(short_account_number)
			
			if check_number:
				check_number = add_zeroes_for_micr_code(check_number)

			if branch_code:
				branch_code = add_zeroes_for_bank_code(branch_code)


			if micr_code is not None and short_account_number is not None:
				row["Unique_number"] = micr_code + short_account_number
				frappe.errprint(row["Unique_number"])
				unique_account_number_lst.append(row.get("Unique_number"))
				frappe.errprint(unique_account_number_lst.append(row.get("Unique_number")))
			
			if micr_code is not None and short_account_number is not None and branch_code is not None and check_number is not None:
				row["Unique_code_for_row"] = check_number + micr_code + short_account_number + branch_code
				unique_account_number_lst.append(row.get("Unique_number"))
				unique_code_list_for_row.append({"slip_number":row["slip_number"],"Unique_code_for_row":row["Unique_code_for_row"]})
			

		
		bank_name_lst = []
		bank_dict = []
		
		for value in set(unique_account_number_lst):
			bank_donar_details = frappe.db.get_all("Donor Bank detail",{"unique_account_number__":value}, ["bank_account","unique_account_number__"] )
			frappe.errprint(bank_donar_details)

			[ bank_dict.append(row) for row in bank_donar_details if row ]
			[bank_name_lst.append(row.get("bank_account")) for row in bank_donar_details if row.get("bank_account")]
		

		
		slip_data = merged_dict_(filter_dict,bank_dict)
		donar_id_lst = []
		bank_details_lst = []
		frappe.errprint(bank_details_lst)
		for row in set(bank_name_lst):
			bank_details = frappe.db.get_all("Bank Account",{"name":row}, ["name","donor_id","bank_account_no"])

			if bank_details:
				bank_details_lst.append(bank_details[0])
				

		[ donar_id_lst.append(row.get("donor_id")) for row in bank_details_lst if row.get("donor_id") ]
		


		slip_data = map_donar_id_with_bank_account(slip_data,bank_details_lst)



		for row in slip_data:
			if row.get("bank_account"):
				bank_details = frappe.db.get_all("Bank Account",{"name":row.get("bank_account")},["name","donor_id","bank_account_no"])
				if bank_details:
					if bank_details[0].get("name") == row.get("bank_account"):
						row["bank_account_no"] = bank_details[0].get("bank_account_no")
		
		donar_details_lst = []
		for value in set(donar_id_lst):
			donar_details= frappe.db.get_all("Donor",{"name":value}, ["name","donor_name" ,"middle_name" ,"last_name"])
			if donar_details:
				donar_details_lst.append(donar_details[0])


		filter_dict = donar_to_full_name(slip_data,donar_details_lst)


		list_for_blocked_donar_details = []
		
		for row in filter_dict:
			if row.get("bank_account"):
				row["bank_account"] = row.get("bank_account")
			if row.get("date_of_slip"):	
				# Convert to datetime object
				date_object = datetime.strptime(row.get("date_of_slip"), '%d-%b-%y %I:%M:%S %p')
				# Format to desired string format
				formatted_date = date_object.strftime('%Y-%m-%d')			
				row["date_of_slip"] = formatted_date

			if row.get("slip_number"):
				if row.get("slip_number").startswith("RC-NB"):
					if micr_code is not None and short_account_number is not None and branch_code is not None and check_number is not None:
						row["Unique_code_for_row"] = check_number + micr_code + short_account_number + branch_code
						unique_account_number_lst.append(row.get("Unique_number"))
						Unique_code_for_row.append(row.get("Unique_code_for_row"))
					list_for_blocked_donar_details.append(row.get("donor_id"))
			


			for row in set(list_for_blocked_donar_details):
				donor_doc = frappe.get_doc("Donor",{"name":row})
				donor_doc.block_status = "Blocked"
				donor_doc.remarks1 = "User has been blocked"
				donor_doc.save()
			


		unique_code_for_rows = []
		for row in unique_code_list_for_row:
			if row.get("slip_number").startswith("RC"):
				unique_code_for_rows.append(row)
				slip_form_check_form = frappe.db.get_all("Slip Cheque Form",{"unique_row_identifier":row.get("Unique_code_for_row")},["unique_row_identifier","slip_number","srno"])
				for rows in filter_dict:	
					if rows.get("slip_number") == row.get("slip_number"):
						rows["ref_link"] = slip_form_check_form[0].get("slip_number")
						rows["ref_id_sr_number"] = str(slip_form_check_form[0].get("srno"))
			
			

		unique_code_identifier_ = []
		for row in filter_dict:
			if row.get("Unique_code_for_row"):
				slip_form_check_form = frappe.db.get_all("Slip Cheque Form",{"unique_row_identifier":row.get("Unique_code_for_row")},["unique_row_identifier","slip_number"])		
				if slip_form_check_form:
					unique_code_identifier_.append(slip_form_check_form[0])
		
		for row in unique_code_identifier_:
			slip_form  = frappe.get_doc("Slip Form",{"name":row.get("slip_number")})
			for check in slip_form.cheque_details:
				for return_check in unique_code_for_rows:
					if check.unique_row_identifier == return_check.get("Unique_code_for_row"):
						if check.clearing_status == "DEPOSITED":
							check.clearing_status = "RETURNED"
							check.ref_link = return_check.get("slip_number")
			slip_form.save()
		
		for row in filter_dict:
			if row.get("donor_id"):
				donar_details = frappe.db.get_all("Donor",{"name":value}, ["name","block_status"])
				if donar_details[0]:
					row["block_status"] = donar_details[0].get("block_status")
		
		for row in filter_dict:
			image_path = row.get("check_path_number").split("/")
			row["image_path"] = image_path[2]
		return filter_dict,slip_number_lst



def crete_entries_in_slip_form(filter_dict,slip_number_lst):
	slip_number_created = []
	existing_slip_number = []
	slip_number_lst_created_ = frappe.db.get_all("Slip Form",["slip_number"])
	
	for row in slip_number_lst_created_:
		existing_slip_number.append(row.get("slip_number"))
	
	slip_number_created = []
	filter_dict.sort(key=itemgetter('slip_number'))  # Ensure data is sorted based on the grouping key
	grouped_data = {key: list(group) for key, group in groupby(filter_dict, key=itemgetter('slip_number'))}
	for slip_number,group_data in grouped_data.items():
		
		if slip_number not in  existing_slip_number:
			slip_exists = frappe.db.exists("Slip Form", {"slip_number": slip_number})
			if slip_exists:
				slip_form_doc = frappe.get_doc("Slip Form", {"slip_number": slip_number})
			else:
				slip_form_doc = frappe.new_doc("Slip Form")
				slip_form_doc.slip_number = slip_number
				#slip_form_doc.slip_event_code = doc.event_master
				slip_form_doc.deposit_account = group_data[0].get("bank_accounts")
				slip_form_doc.slip_event_code = group_data[0].get("event_master")
				slip_form_doc.deposit_bank = group_data[0].get("account_name")
				slip_form_doc.slip_date = group_data[0].get("slip_date")
			for sr_number , row  in  enumerate(group_data):
				sr_number = sr_number + 1
				slip_form_doc.append("cheque_details",{
					"event":group_data[0].get("event_master"),
					"check_image":row.get("check_path_number"), 
					"srno":sr_number,
					"slip_number":slip_number,
					"token":slip_number,
					"image":row.get("image_path"),
					"cheque_image_file_name":row.get("check_path_number"),
					"ref_link":row.get("ref_link"),
					"cheque_number": row.get("check_number"),
					"micr_code": row.get("micr_code"),
					"branch_code": row.get("branch_code"),
					"short_code": row.get("short_account_number"),
					"donor_id_number":row.get("donor"),
					"cheque_bank":row.get("cheque_bank"),
					"donor_name": row.get("donor_name"), 
					"donor_status": row.get("donor_status"),
					"cheque_date": row.get("date_of_slip"),
					"account_no":row.get("account_no"),
					"clearing_status":"CREATED",
					"missing_check_details":row.get("missing_check_"),
					"unique_row_identifier":row.get("Unique_code_for_row"),
					"ref_id_sr_number":row.get("ref_id_sr_number"),
					"donor_status":row.get("donor_status")
				})
			slip_number_created.append(slip_number)	
			slip_form_check_form = frappe.db.get_all("Slip Cheque Form",{"unique_row_identifier":row.get("Unique_code_for_row") },["name"])
			
			for check in slip_form_check_form:
				frappe.db.set_value("Slip Cheque Form",check.get("name"),"ref_id_sr_number",sr_number)
			slip_form_doc.save()	
			frappe.errprint(slip_form_doc)

	return len(slip_number_created)
			
	

			
@frappe.whitelist()
def read_csv(file,doc):
	
	file_doc = frappe.get_doc("File",{"file_url":file})
	file_url = file_doc.file_url
	# file_path = frappe.utils.get_files_path(file_doc.file_name)
	file = get_absolute_path(file_url)
	doc = json.loads(doc)
	event_master = doc.get("event_master")
	bank_accounts = doc.get("bank_accounts")
	account_name = doc.get("account_name")
	slip_date = doc.get("slip_date")
	df = pd.read_csv(file,names=['A', 'B', 'C'])
	dict_list = df.to_dict('records')
	
	for row in dict_list:
		row["bank_accounts"] = bank_accounts
		row["event_master"] = event_master
		row["account_name"] = account_name
		row["slip_date"] = slip_date
	
	filter_dict,slip_number_lst = read_csv_(dict_list,df)

	return crete_entries_in_slip_form(filter_dict, slip_number_lst)
	
	


def get_absolute_path(file_name):
	
	file_path = ""
	if(file_name.startswith('/files/')):
		file_path += f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
	if(file_name.startswith('/private/')):
		file_path += f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
	return file_path	
	
	
	
	
def merged_dict_(slip_data,bank_data):
	
	# Create a dictionary to map unique numbers to bank accounts
	unique_to_bank = {bank['unique_account_number__']: bank['bank_account'] for bank in bank_data}
	# Update slip_data with bank_account where Unique_number matches
	for slip in slip_data:
		unique_number = slip.get('Unique_number')
		bank_account = unique_to_bank.get(unique_number)

		if bank_account:
			slip['bank_account'] = bank_account
	
	return  slip_data




def map_donar_id_with_bank_account(slip_data,bank_data):
	# Create a dictionary to map bank account numbers to donor ids
	bank_number_to_donor_id = {bank['name']: bank['donor_id'] for bank in bank_data}
	# Update slip_data with donor_id where bank_account matches bank_account_no
	for slip in slip_data:
		bank_account_name = slip.get('bank_account')
		if bank_account_name:
			donor_id = bank_number_to_donor_id.get(bank_account_name)
			if donor_id:
				slip['donor_id'] = donor_id
		return slip_data


			
					






def donar_to_full_name(slip_data,bank_data):
	# Create a dictionary to map donor_id to full_name
	donor_id_to_full_name = {}
	# Iterate through new_data to create the mapping
	for donor in bank_data:
			full_name_parts = [donor.get('donor_name', ''), donor.get('middle_name', ''), donor.get('last_name', '')]
			full_name = ' '.join(part if part else ' ' for part in full_name_parts).strip()
			donor_id = donor.get('name')
			donor_id_to_full_name[donor_id] = full_name
	# Update slip_data with full_name where donor_id matches
	for slip in slip_data:
		donor_id = slip.get('donor_id')
		full_name = donor_id_to_full_name.get(donor_id)
		if full_name:
			slip['full_name'] = full_name


	return slip_data



def add_zeroes_for_micr_code(str_num):
    num_length = len(str_num)
    num_zeroes = 9 - num_length
    return '0' * num_zeroes + str_num

def fetch_bank_account(micr_code, short_account_number):
    bank_account_details = frappe.db.get_all("Bank Account",
                                            filters={"micr": micr_code,
                                                    "short_account_number": short_account_number},
                                            fields=["name"])
    frappe.errprint(bank_account_details)

def add_zeroes_for_short_account_number(str_num):
    num_length = len(str_num)
    num_zeroes = 6 - num_length
    return '0' * num_zeroes + str_num


def add_zeroes_for_bank_code(str_num):
    num_length = len(str_num)
    num_zeroes = 2 - num_length
    return '0' * num_zeroes + str_num	
		
		
	
	



	

	

























