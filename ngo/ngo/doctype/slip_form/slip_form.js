// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Slip Form', {
	refresh:function(frm){

				

	},
	cheque_details_on_form_rendered: function(frm, cdt,cdn){


	    
	    // $('.previous').remove();
        // $('.row-actions').append("<button class='btn btn-secondary btn-sm previous'>Previous</button> &nbsp;");
        // $(".previous").off('click').on('click', function(){
        //     cur_frm.open_grid_row().open_prev();
        // });
	    
	    
	    // // Check if the button already exists before appending it
	    // $('.next').remove();
        // $('.row-actions').append("<button class='btn btn-secondary btn-sm next'>Next</button> &nbsp;&nbsp;");
        // $(".next").off('click').on('click', function(){
        //     cur_frm.open_grid_row().open_next();
        // });

        
        
	

	},



});


frappe.ui.form.on('Slip Cheque Form', {
    next: function(frm,cdt,cdn) {
        var cheque_details = cur_frm.doc.cheque_details;
        var child = locals[cdt][cdn];
        var current_row_idx = child.idx
        
        if (current_row_idx < cheque_details.length) {
            // Open the next row in the grid
            cur_frm.open_grid_row().open_next();
        } 
        
        else 
			{ 

				frappe.msgprint("All rows have been opened.");
			
			}
    },

    previous: function(frm) {
        cur_frm.open_grid_row().open_prev();
    }
});













