import frappe

@frappe.whitelist()
def get_territory_tree_from_locality(locality):
  res = [None, None, None, None]

  res[0] = frappe.db.get_value("Territory", locality, "parent_territory")
  res[1] = frappe.db.get_value("Territory", res[0], "parent_territory")
  res[2] = frappe.db.get_value("Territory", res[1], "parent_territory")
  res[3] = frappe.db.get_value("Territory", res[2], "parent_territory")

  return res