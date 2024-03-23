# Copyright (c) 2024, smb and contributors
# For license information, please see license.txt
import pandas as pd
import re
import frappe
from frappe.model.document import Document
from datetime import datetime
import os

import requests

class SlipScannerFilePath(Document):
	def autoname(self):
		now = datetime.now()
		custom_name = now.strftime("%d:%m:%y:%H:%M")
		self.name = custom_name 
	


def read_csv_(dict_list):
		
		filter_dict = []
		slip_number_lst = []
		missing_check_details = []

		for row in dict_list:
			date_of_slip = row.get("A")  # Extract date_of_slip from dictionary
			number = row.get("B")  # Extract number from dictionary
			slip_number = None  # Initialize slip_number to None
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
							"check_path_number":number

						})
						
					else:

						filter_dict.append({
							"date_of_slip": date_of_slip,
							"slip_number": slip_number,
							"missing_check_":number,
							"check_path_number":number

						})

						missing_check_details.append(number)


		df = pd.read_csv("/home/milind/Downloads/SVS_ScannedCheques267c79(1).csv",names=['A', 'B', 'C'])

		check_details_list = df['B'].tolist()



		list_of_check_number = []
		for row in filter_dict:
			list_of_check_number.append(row.get("check_path_number"))

		

		for value in check_details_list:
			if value not in list_of_check_number:
				print(value,"===-----==")



		unique_account_number_lst = []
		for row in filter_dict:
			micr_code = row.get("micr_code")
			short_account_number = row.get("short_account_number")
			branch_code = row.get("branch_code")
			if micr_code is not None and short_account_number is not None and branch_code is not None:
				row["Unique_number"] = micr_code + short_account_number + branch_code
				unique_account_number_lst.append(row.get("Unique_number"))
			
		
		bank_name_lst = []
		bank_dict = []


		for value in set(unique_account_number_lst):
			bank_donar_details = frappe.db.get_all("Donor Bank detail",{"unique_account_number__":value}, ["bank_account","unique_account_number__"] )
			[ bank_dict.append(row) for row in bank_donar_details if row ]
			[bank_name_lst.append(row.get("bank_account")) for row in bank_donar_details if row.get("bank_account")]
		slip_data = merged_dict_(filter_dict,bank_dict)

		



		donar_id_lst = []
		bank_details_lst = []

		for row in set(bank_name_lst):
			bank_details = frappe.db.get_all("Bank Account",{"name":row}, ["name","donor_id","bank_account_no"])
			
			if bank_details:
				bank_details_lst.append(bank_details[0])
			


		[ donar_id_lst.append(row.get("donor_id")) for row in bank_details_lst if row.get("donor_id") ]
		slip_data = map_donar_id_with_bank_account(slip_data,bank_details_lst)


		donar_details_lst = []

		for value in set(donar_id_lst):
			donar_details= frappe.db.get_all("Donor",{"name":value}, ["name","donor_name" ,"middle_name" ,"last_name"])

			if donar_details:
				donar_details_lst.append(donar_details[0])


		filter_dict = donar_to_full_name(slip_data,donar_details_lst)

		for row in filter_dict:
			if row.get("bank_account"):
				row["bank_account"] = row.get("bank_account").split("-")[0]

			if row.get("date_of_slip"):
				# Convert to datetime object
				date_object = datetime.strptime(row.get("date_of_slip"), '%d-%m-%y %H:%M')	
				# Format to desired string format
				formatted_date = date_object.strftime('%Y-%m-%d')

				row["date_of_slip"] = formatted_date


		# return filter_dict,slip_number_lst


				


	
def crete_entries_in_slip_form(filter_dict,slip_number_lst):
	
	existing_slip_number = []
	
	slip_number_lst_created_ = frappe.db.get_all("Slip Form",["slip_number"])
	
	for row in slip_number_lst_created_:
		existing_slip_number.append(row.get("slip_number"))

	slip_number_created = []
	
	for slip_number in slip_number_lst:
		if slip_number not in  existing_slip_number:
			frappe.msgprint("Records Creation Started")          
			for row in filter_dict:
				slip_number = row.get("slip_number")
				slip_exists = frappe.db.exists("Slip Form", {"slip_number": slip_number})
				if slip_exists:
					slip_form_doc = frappe.get_doc("Slip Form", {"slip_number": slip_number})
					sr_number = len(slip_form_doc.cheque_details) + 1 
					slip_form_doc.append("cheque_details",{
						"srno":sr_number,
						"cheque_number": row.get("check_number"),
						"micr_code": row.get("micr_code"),
						"branch_code": row.get("branch_code"),
						"short_code": row.get("short_account_number"),
						"donor_id_number":row.get("donor_id"),
						"bank_account": row.get("account_no"),
						"donor_name": row.get("full_name"),       
						"cheque_date": row.get("date_of_slip"),
						"account_no":row.get("bank_account"),
						"clearing_status":"CREATED" 

					})
					slip_number_ = row.get("slip_number")
					slip_form_doc.save()
				else:
					slip = frappe.new_doc("Slip Form")
					slip_number = row.get("slip_number")
					slip.slip_number = slip_number
					slip.append("cheque_details", {
						"srno":1,
						"cheque_number": row.get("check_number"),
						"micr_code": row.get("micr_code"),
						"branch_code": row.get("branch_code"),
						"short_code": row.get("short_account_number"),
						"donor_id_number":row.get("donor_id"),
						"bank_account": row.get("account_no"),
						"donor_name": row.get("full_name"),       
						"cheque_date": row.get("date_of_slip"),
						"account_no":row.get("bank_account"), 
						"clearing_status":"CREATED"

					})
					
					slip.insert()
					slip_number_ = row.get("slip_number")
					slip_number_created.append(slip_number)			
	
	
	return len(slip_number_created)


	






			
@frappe.whitelist()
def read_csv(file):
	
	file_doc = frappe.get_doc("File",{"file_url":file})
	
	file_url = file_doc.file_url

	# file_path = frappe.utils.get_files_path(file_doc.file_name)

	file = get_absolute_path(file_url)

	df = pd.read_csv(file,names=['A', 'B', 'C'])

	dict_list = df.to_dict('records')

	# df = df.rename(columns={'A': 'Date_Time', 'B': 'check_details', 'C': 'bank_details'})
	# df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%d-%m-%y %H:%M')
	# df.insert(0, 'Date', df['Date_Time'].dt.date)
	# df.drop(columns=['Date_Time'], inplace=True)
	# pattern = r'\\([^\\$]+)\$'
	# df['Slip_number'] = df['check_details'].str.extract(pattern)
	# df['Bank_Details_Split'] = df['bank_details'].str.split('<')
	# for row in dict_list:
	# 	Bank_Details_Split = row.get("Bank_Details_Split")
	# 	print()
	# 	# Bank_Details_Split= [value  for value in Bank_Details_Split if value]
	# 	Bank_Details_Split = ",".join(Bank_Details_Split)
	# 	Bank_Details_Split = Bank_Details_Split.split(":")
	# 	Bank_Details_Split = ",".join(Bank_Details_Split)
	# 	Bank_Details_Split = Bank_Details_Split.split(",")
	# 	row["Bank_Details_Split"] = Bank_Details_Split
	
	


	filter_dict,slip_number_lst = read_csv_(dict_list)
	
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
	bank_number_to_donor_id = {bank['bank_account_no']: bank['donor_id'] for bank in bank_data}
	
	# Update slip_data with donor_id where bank_account matches bank_account_no
	for slip in slip_data:
		bank_account_name = slip.get('bank_account')
		
		


		bank_account_number = bank_account_name.split(" - ")[0]  # Extract the bank account number
		donor_id = bank_number_to_donor_id.get(bank_account_number)
	
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





		
		
		
	
	



	

	


























