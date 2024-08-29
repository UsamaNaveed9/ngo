import frappe

def execute():
  frappe.db.delete("Workspace", "NGO 1")
  frappe.db.delete("Workspace", "NGO Test")