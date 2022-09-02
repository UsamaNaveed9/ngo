import frappe
from ngo.utils import createAPIErrorLog

@frappe.whitelist()
def get_center_list():
    try:
        filters={}
        kendra_list = frappe.db.get_list('Kendra',
                filters= filters,
                fields=['name'],
                order_by='name asc'
            )
        return kendra_list
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def get_kendra_jawabdar():
    try:
        filters={}
        kjs_list = frappe.db.get_list('Kendra Jawabdar',
                filters= filters,
                fields=['name']
            )
        for kendra_jawabdar in kjs_list :
            center_list =   frappe.db.get_list('Kendra Jawabdar Centre',
                filters= filters,
                fields=['name']
            )          
        
        return kendra_list
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error