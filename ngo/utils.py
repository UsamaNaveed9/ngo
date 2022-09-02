# -*- coding: utf-8 -*-
# Copyright (c) 2020, Leader Investment Group

import json
import requests
import frappe
import inspect

def createAPIErrorLog(error):
    error_log =  frappe.new_doc("Error Log")
    error_log.method = inspect.stack()[1][3] 
    error_log.error = error
    error_log.save(ignore_permissions=True)