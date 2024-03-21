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
                fields=['name','first_name','last_name']
            )
        kendra_jawabdar_and_center_data = []
        for kendra_jawabdar in kjs_list :
            kendra_jawabdar_and_center_filter= {"parent":kendra_jawabdar.get("name")}
            kendra_jawabdar_and_center_data.append({
                kendra_jawabdar.get("first_name")+ " " + kendra_jawabdar.get("last_name"):{
                    "center_list":frappe.db.get_list('Kendra Jawabdar Center',filters= kendra_jawabdar_and_center_filter,fields=['kendra']),
                    "first_name": kendra_jawabdar.get("first_name"),
                    "last_name": kendra_jawabdar.get("last_name")
                }
            })
        return kendra_jawabdar_and_center_data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def get_donor_list():
    try:
        filters={}
        donar_data = frappe.db.get_list('Donor',
                filters= filters,
                fields=['*'],
                order_by='name asc'
            )
        for donar in donar_data:
            donar["account_details"] = frappe.db.get_list('Donor Bank detail',
                filters= {"parent":donar.get("name")},
                fields=['bank_account','is_default']
            )
            print("*********",donar["account_details"]  )
    

        return donar_data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error


@frappe.whitelist()
def create_update_donor(data, donor_id=None):
    try:
        if not donor_id:
            donor = frappe.new_doc("Donor")
        else:
            donor = frappe.get_doc("Donor", donor_id)
        donor.donor_name =  data.get("first_name")#m
        donor.donor_type =  data.get("donor_type")#m  #l
        donor.mobile_number =  data.get("mobile_number")#m
        donor.aadhar =  data.get("aadhar")#m
        donor.email =  data.get("email") #m
        donor.pan_number =  data.get("pan_number") #m #new

        if data.get("middle_name"):
            donor.middle_name =  data.get("middle_name")
        if data.get("country_code"):
            donor.country_code =  data.get("country_code") #l
        if data.get("kendra"):
            donor.kendra =  data.get("kendra") #l
        if data.get("country"):
            donor.country =  data.get("country") #l
        if data.get("region"):
            donor.region =  data.get("region") #l
        if data.get("district"):
            donor.district =  data.get("district") #l 
        if data.get("zone"):
            donor.zone =  data.get("zone")  #l
        if data.get("center"):
            donor.locality =  data.get("center") #l
        if data.get("passport_issued_by_country"):
            donor.passport_issued =  data.get("passport_issued_by_country")#l
        if data.get("otp_verified"):
            donor.verified =  data.get("otp_verified")
        if data.get("passport_number"):
            donor.passport_number =  data.get("passport_number")
        if data.get("passport_valid"):
            donor.passport_valid =  data.get("passport_valid")
        
        donor.set('account', [])
        for account_entry in data.get('accounts'):
            donor_account = donor.append('account', {})
            donor_account.bank_account = account_entry.get("bank_account")
       
        donor.save(ignore_permissions=True)
        frappe.db.commit()
        return donor.name
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error