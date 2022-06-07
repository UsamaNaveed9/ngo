// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Details', {
	setup: function(frm) {
		frm.set_query("deposit_account", function(){
		    return {
		        filters: [
		            ["Bank Account","is_company_account","=", "1"]
		        ]
		    }
		});
	}
});
