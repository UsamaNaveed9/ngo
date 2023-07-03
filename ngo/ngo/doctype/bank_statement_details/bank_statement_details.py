# -*- coding: utf-8 -*-
# Copyright (c) 2022, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.model.document import Document

class BankStatementDetails(Document):
	def on_submit(self):
		for i in self.statement_details:
			# Reduce to 6 digits if longer
			if len(str(i.cheque_no)) > 6:
				i.cheque_no = str(i.cheque_no)[-6:]
			else:
				# Add leading zeros if shorter
				i.cheque_no = str(i.cheque_no).zfill(6)
			if len(str(i.san)) > 6:
				i.san = str(i.san)[-6:]
			else:
				i.san = str(i.san).zfill(6)
			i.code = str(i.cheque_date)+str(i.cheque_no)+str(i.micr)+str(i.san)+str(i.branch_code)+str(i.amount)
			i.amount_mis_code = str(i.cheque_date)+str(i.cheque_no)+str(i.micr)+str(i.san)+str(i.branch_code)
			i.micr_mis_code = str(i.cheque_date)+str(i.cheque_no)+str(i.san)+str(i.branch_code)+str(i.amount)
			i.cheque_no_mis_code = str(i.cheque_date)+str(i.micr)+str(i.san)+str(i.branch_code)+str(i.amount)
			i.san_mis_code = str(i.cheque_date)+str(i.cheque_no)+str(i.micr)+str(i.branch_code)+str(i.amount)
		self._save()	

	def submit(self):
		if len(self.statement_details) > 5:
			msgprint(_("The Code Generation task of each record has been enqueued as a background job. In case there is any issue on processing in background, the system will add a comment about the error on this Bank Statement Details and revert to the Draft stage"))
			self.queue_action('submit', timeout=40000)
		else:
			self._submit()

	