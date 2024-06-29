import frappe
import csv

def execute():
  csv_output = [["Donor", "Bank Account"]]

  frappe.db.delete("Donor Bank detail")

  donors = frappe.db.get_list("Donor")

  for i in donors:
    donor = frappe.get_doc("Donor", i.name)

    bank_accounts = frappe.db.get_list("Bank Account", filters={
      "donor_id": donor.name
    }, fields=["name", "bank"])

    for bank_account in bank_accounts:
      donor.append("account", {
        "bank": bank_account.bank,
        "bank_account": bank_account.name,
      })
      csv_output.append([donor.name, bank_account.name])
    
    donor.save()

  with open(frappe.get_site_path() + "/Donor_Bank_Account_Fixed.csv", "w") as f:
    writer = csv.writer(f)

    writer.writerows(csv_output)
