// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bank Statement Details', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		frm.set_query('bank_account', function(doc) {
			return {
				filters: {
					'is_company_account': 1,
				}
			}
		});
	}
});
