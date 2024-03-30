// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Slip Form', {
	refresh:function(frm){
        


        var slip_number = cur_frm.doc.slip_number
        var deposit_date = cur_frm.doc.deposit_date
        
        if (slip_number && deposit_date ){
            var parts = deposit_date.split("-");
            var newDateStr = parts[2] + "-" + parts[1] + "-" + parts[0].slice(-2);
            var new_code = slip_number + "-" + newDateStr
            frm.set_value("slip_event_code",new_code)

        }
        
        var cheque_details = frm.doc.cheque_details;
        frm.set_value("number_of_cheques_in_slip",cheque_details.length)
        var total_amount = 0
        var totalAmountDeposited = 0;
        var totalNumberOfCheckDeposited = []
        var number_of_cheques_returned_or_rejected_in_slip_lst = []
        $.each(cheque_details, function(index, value) {

            total_amount += parseFloat(value.amount);


            if (value.clearing_status === "DEPOSITED") {
                totalAmountDeposited += parseFloat(value.amount);
                totalNumberOfCheckDeposited.push(value.clearing_status)
            }

            if (value.clearing_status === "RETURNED"){
                number_of_cheques_returned_or_rejected_in_slip_lst.push(value.clearing_status)

            }
              
        });

        frm.set_value("total_amount_in_slip",total_amount) 
        
        frm.set_value("number_of_cheques_returned_or_rejected_in_slip",number_of_cheques_returned_or_rejected_in_slip_lst.length)
        
        frm.set_value("number_of_cheques_deposited_in_slip",totalNumberOfCheckDeposited.length)
        
        frm.set_value("total_amount_of_deposited_cheques",totalAmountDeposited)

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













