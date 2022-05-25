// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event Master', {
	before_save: function(frm){
		if(frm.doc.extend_ends_on){
			if(frm.doc.ends_on){
				frm.set_value('status', 'Extended');
			}
		}
	}
});
