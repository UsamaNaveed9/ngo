// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Slip Form', {
	refresh:function(frm){
		

	}

});


frappe.ui.form.on('Slip Cheque Form',{
	refresh:function(frm){
		
	},
    next:function(frm){
        cur_frm.open_grid_row().open_next();
    },
    previous:function(frm){
        // $('[data-fieldname="cheque_details"]').find('[data-idx="3"] .btn-open-row').click()
        cur_frm.open_grid_row().open_prev();
    }
});












