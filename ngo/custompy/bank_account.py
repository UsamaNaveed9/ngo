import frappe

def before_save(doc, method=None):
  old_donor_id = frappe.db.get_value("Bank Account", doc.name, "donor_id")
  if old_donor_id != doc.donor_id:
    # Set Bank account in Updated Donor
    new_donor = frappe.get_doc("Donor", doc.donor_id)

    if doc.name not in [i.bank_account for i in new_donor.account]:
      new_donor.append("account", {
        "bank": doc.bank,
        "bank_account": doc.name,
      })

      new_donor.save()

    # Remove Bank Account in Old donor
    frappe.db.delete("Donor Bank detail", {
      "bank_account": doc.name,
      "parenttype": "Donor",
      "parent": old_donor_id
    })