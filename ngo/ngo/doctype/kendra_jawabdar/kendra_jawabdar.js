// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kendra Jawabdar', {
	setup(frm) {
		frm.fields_dict['list_of_authorized_centres'].grid.get_field("centres").get_query = function(doc, cdt, cdn) {
	    return {
		    filters: [
			    ['Territory', 'is_group', '=','0'],
		    ]
	    }
        }
	}
});
