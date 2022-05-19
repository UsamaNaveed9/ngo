# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from datetime import datetime
from pytz import timezone 

__version__ = '0.0.1'


@frappe.whitelist()
def update_event_status():
	now = datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
	#print ("Current date and time : ", now)

	event_not_started = frappe.db.get_list('Event Master',
    filters={
        'status': 'Not Started'
    },
    fields=['name','starts_on','ends_on']
	)

	#print(event_not_started)
	for i in event_not_started:
		starts_on = i.starts_on.strftime("%Y-%m-%d %H:%M:%S")
		ends_on = i.ends_on.strftime("%Y-%m-%d %H:%M:%S")
		#print(starts_on, ends_on)
		if now > starts_on:
			doc = frappe.get_doc('Event Master', i.name)
			doc.status = 'Started'
			doc.save()
			#print("Done")
		 
	event_started = frappe.db.get_list('Event Master',
    filters={
        'status': 'Started'
    },
    fields=['name','starts_on','ends_on']
	)
	for i in event_started:
		starts_on = i.starts_on.strftime("%Y-%m-%d %H:%M:%S")
		ends_on = i.ends_on.strftime("%Y-%m-%d %H:%M:%S")
		#print(starts_on, ends_on)
		if now > ends_on:
			doc = frappe.get_doc('Event Master', i.name)
			doc.status = 'Closed'
			doc.save()
			#print("Done")

