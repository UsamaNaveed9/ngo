// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Slip Form', {
    refresh:function(frm){
        frm.add_custom_button(__('Select Blocked Donor'),function(){
                // Iterate over each row in the grid
                var block_donor = []
                $.each(frm.doc.cheque_details, function(index, row) {
                    // Check if the row meets your condition, for example, if donor_status is "Blocked"
                    if (row.donor_status == "Blocked"){
                        $('*[data-fieldname="cheque_details"]').find('.grid-row-check')[index+1].click()
                        block_donor.push(row.donor_status)    
                    }
                });
            frappe.msgprint(__("{0}  Row  Selected  For delete ", [block_donor.length]));
        },__("DELETE"));
        frm.add_custom_button(__('Delete Blocked Donor'),function(){
              frappe.confirm('Are you sure you want Delete Row',
                    () => {
                        var grid = frm.fields_dict['cheque_details'].grid;
                        var selected_rows = grid.get_selected_children();
                        grid.delete_rows(selected_rows)

                    }, () => {
                        
                    })  
        },__("DELETE"));
    $("button[data-original-title=Print]").hide();
    frm.add_custom_button(__('Print Slip'),function(){
        var cheque_details = frm.doc.cheque_details;
        var current_date = frappe.datetime.now_date();
        frm.set_value("deposit_date",current_date)
        frm.set_value("slip_deposited_status","Yes")
        var block_donor = []
        $.each(cheque_details, function(index, value){
            value.clearing_status = "DEPOSITED";
            if(value.amount == 0){
                frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
            }
        });

        var print_format_id = frm.doc.name;
        var formated_url = "/api/method/frappe.utils.print_format.download_pdf?doctype=Slip Form&name=" + print_format_id + "&format=Slip-1&no_letterhead=1&letterhead=No Letterhead&settings={}&_lang=en-US"
        window.open(formated_url);
        
        frappe.msgprint("Clearing Status DEPOSITED Applied");
        },__("Print"));
    frm.add_custom_button(__('Print Detailed Slip'),function(){
        var cheque_details = frm.doc.cheque_details;
        var current_date = frappe.datetime.now_date();

        frm.set_value("deposit_date",current_date)
        frm.set_value("slip_deposited_status","Yes")
        var block_donor = []
        $.each(cheque_details, function(index, value){
            value.clearing_status = "DEPOSITED";
            if(value.amount == 0){
                frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
            }
        });
        var print_format_id = frm.doc.name;
        var formated_url = "/api/method/frappe.utils.print_format.download_pdf?doctype=Slip Form&name=" + print_format_id + "&format=Slip-2&no_letterhead=1&letterhead=No Letterhead&settings={}&_lang=en-US"
        window.open(formated_url);
        frappe.msgprint("Clearing Status DEPOSITED Applied");
        },__("Print"));
    },
    validate:function(frm){
        var slip_number = cur_frm.doc.slip_number
        var deposit_date = cur_frm.doc.deposit_date
        if (slip_number && deposit_date ){
            var parts = deposit_date.split("-");
            var newDateStr = parts[2] + "-" + parts[1] + "-" + parts[0].slice(-2);
            var new_code = slip_number + "-" + newDateStr
            frm.set_value("internal_slip_number",new_code)

        }
        var cheque_details = frm.doc.cheque_details;
        if (cheque_details){    
            frm.set_value("number_of_cheques_in_slip",cheque_details.length)
        }
        var total_amount = 0
        var totalAmountDeposited = 0;
        var totalNumberOfCheckDeposited = []
        var number_of_cheques_returned_or_rejected_in_slip_lst = []
        $.each(cheque_details, function(index, value){
            total_amount += parseFloat(value.amount);
            if (value.clearing_status === "DEPOSITED") {
                totalAmountDeposited += parseFloat(value.amount);
                totalNumberOfCheckDeposited.push(value.clearing_status)
            }
            if (value.clearing_status === "RETURNED"){
                number_of_cheques_returned_or_rejected_in_slip_lst.push(value.clearing_status)
            }
            if (cur_frm.doc.slip_number.startsWith("RC")){                               
                value.clearing_status = "RETURNED"
            }
            if(value.amount == 0){
                frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
            }
        });
        frm.set_value("total_amount_in_slip",total_amount) 
        frm.set_value("number_of_cheques_returned_or_rejected_in_slip",number_of_cheques_returned_or_rejected_in_slip_lst.length)
        frm.set_value("number_of_cheques_deposited_in_slip",totalNumberOfCheckDeposited.length)
        frm.set_value("total_amount_of_deposited_cheques",totalAmountDeposited)
    },
    cheque_details_on_form_rendered:function(frm,cdt,cdn){

        // $('[data-fieldname="form-grid"]').on('keydown', function(event) {


        //     // Check if the pressed key is the right arrow key (key code 39)
        //     if (event.keyCode === 39) {
        //         // Call the open_prev() method
        //         cur_frm.open_grid_row().open_prev();
        //     }
        // }); 

        
        
        var cheque_details_len = frm.doc.cheque_details.length
        var newDiv = $('<div>').text('Total Number Of Checks: ' + cheque_details_len);

        newDiv.css({
               'font-size': '20px',
               'color': 'red'
           });
        
        $('[data-fieldname="total_row_count"]').empty().append(newDiv);
        
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-insert-row-below').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-delete-row').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-insert-row').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-duplicate-row').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-move-row').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-collapse-row').hide();
        frm.fields_dict["cheque_details"].grid.wrapper.find('.grid-append-row').hide();

                

                

    }
}); 

frappe.ui.form.on('Slip Cheque Form',{
    next: function(frm,cdt,cdn){
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
    },



    account_no:function(frm,cdt,cdn){
        var child = locals[cdt][cdn];
        var account_no = child.account_no
        if (account_no){

             frappe.call({
                    method: "ngo.ngo.doctype.slip_form.slip_form.get_donor_details_from_account",
                    args: {
                        account_no: account_no
                    },
                    callback: function(r){
                        frappe.model.set_value(child.doctype, child.name, "donor_id_number",r.message.name)
                        frappe.model.set_value(child.doctype, child.name, "donor_name",r.message.full_name)
                    }
                });
        }
       
        },
    donor_id_number:function(frm,cdt,cdn){
        var child = locals[cdt][cdn];
        var donor_id_number = child.donor_id_number
        if (donor_id_number){
           frappe.call({
                method: "ngo.ngo.doctype.slip_form.slip_form.get_donor_details_from_donar_id",
                args: {
                    donor_id_number: donor_id_number
                },
                callback: function(r){
                    if (!child.account_no){
                        frappe.model.set_value(child.doctype, child.name, "account_no",r.message.account_name)    
                    }
                    frappe.model.set_value(child.doctype, child.name, "donor_name",r.message.full_name)
                }
            });

        }
    }


   
});





  






// function get_selected(){
//         // returns list of children that are selected. returns [parentfield, name] for each
//         var selected = {}, me = this;
//         frappe.meta.get_table_fields(this.doctype).forEach(function(df){
//             // handle TableMultiselect child fields
//             let _selected = [];

//             if(me.fields_dict[df.fieldname].grid) {
//                 _selected = me.fields_dict[df.fieldname].grid.get_selected();
//             }

           
//         });
//         return selected;
// }

