# -*- coding: utf-8 -*-
# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.model.document import Document

class SlipDetails(Document):
	def on_submit(self):
		for i in self.cheque_details:
			# Reduce to 6 digits if longer
			if len(str(i.cheque_number)) > 6:
				i.cheque_number = str(i.cheque_number)[-6:]
			else:
				# Add leading zeros if shorter
				i.cheque_number = str(i.cheque_number).zfill(6)
			if len(str(i.short_code)) > 6:
				i.short_code = str(i.short_code)[-6:]
			else:
				i.short_code = str(i.short_code).zfill(6)
			i.code = str(i.cheque_date)+str(i.cheque_number)+str(i.micr_code)+str(i.short_code)+str(i.branch_code)+str(i.amount)
			i.amount_mis_code = str(i.cheque_date)+str(i.cheque_number)+str(i.micr_code)+str(i.short_code)+str(i.branch_code)
			i.micr_mis_code = str(i.cheque_date)+str(i.cheque_number)+str(i.short_code)+str(i.branch_code)+str(i.amount)
			i.cheque_no_mis_code = str(i.cheque_date)+str(i.micr_code)+str(i.short_code)+str(i.branch_code)+str(i.amount)
			i.san_miss_code = str(i.cheque_date)+str(i.cheque_number)+str(i.micr_code)+str(i.branch_code)+str(i.amount)
		self._save()	

	def submit(self):
		if len(self.cheque_details) > 5:
			msgprint(_("The Code Generation task of each record has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this Slip Details and revert to the Draft stage"))
			self.queue_action('submit', timeout=40000)
		else:
			self._submit()
