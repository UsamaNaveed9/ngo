// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Slip Form',{





    refresh:function(frm){

        frm.add_custom_button(__('Select Blocked Donor'), function() {
            // Function to select blocked donors
            select_blocked_donors(frm);
        },__("DELETE"));
        function select_blocked_donors(frm) {
            // Assume 'cheque_details' is the table name in the Payment Entry
            var blocked_donors = frm.doc.cheque_details.filter(cheque => cheque.donor_status === 'Blocked');
            console.log(blocked_donors);
        
            if (blocked_donors.length === 0) {
                frappe.msgprint(__('No blocked donors found'));
                return;
            }
        
            // Update the 'is_block' field for blocked donors
            blocked_donors.forEach(function(cheque) {
                frappe.model.set_value(cheque.doctype, cheque.name, 'is_block', 1);
            });
            frm.save().then(() => {
                frappe.msgprint(__(`{0} blocked donors selected`, [blocked_donors.length]));
            });
            // frm.save()
            // frappe.msgprint(__('{0} blocked donors selected', [blocked_donors.length]));
        }
        frm.add_custom_button(__('Delete Blocked Donor'), function() {
            select_blocked_donors_slip(frm);
            // Check if frm and frm.doc are valid
        }, __("DELETE"));

        function select_blocked_donors_slip(frm) {
            if (frm && frm.doc) {
                // Access required properties safely
                var slip_date = frm.doc.slip_date;
                console.log(slip_date);
        
                // Count the number of blocked donors
                var blocked_count = 0;
                frm.doc.cheque_details.forEach(function(row) {
                    if (row.is_block || row.donor_status === "Blocked") {
                        blocked_count++;
                    }
                });
        
                // Confirm deletion with count
                frappe.confirm(`Are you sure you want to delete ${blocked_count} row(s) with blocked donors?`, function() {
                    // Make the call to the server-side function
                    frappe.call({
                        method: 'ngo.ngo.doctype.slip_form.slip_form.create_deleted_record',
                        args: {
                            docname: frm.doc.name // Pass the document name to the server-side method
                        },
                        callback: function(response) {
                            // Handle the response from the server if needed
                            console.log(response);
                            if (response.message) {
                                frappe.show_alert({
                                    message: __("New Slip Form created: {0}", [response.message]),
                                    indicator: 'green'
                                });
                                
                                frm.set_value("total_amount_in_slip", frm.doc.total_amount_in_slip - blocked_amount);
                                frm.refresh();
                            }
                        }
                    });
                });
            } else {
                // Handle the case when frm or frm.doc is not valid
                console.error('Form or form document is not valid.');
            }
        }

        frm.add_custom_button(__("Sync with Master Data"), function() {
            if(frm.is_dirty()) return frappe.throw("Please save the form!")

            frappe.call({
                method: "ngo.ngo.doctype.slip_form.slip_form.set_donor_from_account",
                args: {
                    slip_form_name: frm.doc.name
                },
                callback: function(r){
                    frm.refresh()
                },
                freeze: true,
                freeze_message: "Setting donor on basis of account number..."
            });
        })
        frm.add_custom_button(__("Validate Cheques"), function() {
            if(frm.is_dirty()) return frappe.throw("Please save the form!")
  
            frm.dashboard.reset()
            frm.dashboard.show()
            var errors = []

            console.log('hit hua')

            frappe.call({
                method: "ngo.ngo.doctype.slip_form.slip_form.validate_cheques",
                type: "POST",
                args: {
                    slip_form_name: frm.doc.name
                },
                callback: function(r) {
                    console.log('api response', r)
                    var errors = r.message
                    console.log('errors', errors)
                    if(errors.length == 0) {
                        frappe.msgprint({
                            title: __('Success'),
                            indicator: 'green',
                            message: __('All Cheques are OK')
                        });
                        return
                    }
                    
                    const newTable = document.createElement("table");
                    newTable.setAttribute("border", "1")
                    newTable.setAttribute("width", "100%")
                    var headers = ['Id', 'Amount', 'Short Code', 'MICR', 'Cheque Number', 'Account Number', 'Donor Id']
                
                    const thead = document.createElement("thead");
                    headers.forEach(header => {
                        const th = document.createElement("th");
                        th.textContent = header;
                        thead.appendChild(th);
                    })
                    newTable.appendChild(thead);
                
                    errors.forEach(error => {
                        const newRow = document.createElement("tr");
                        headers.forEach(header => {
                            const td = document.createElement("td");
                            td.textContent = error[header] || "OK";
                            newRow.appendChild(td);
                        })
                        newTable.appendChild(newRow);
                    })
                    
                    console.log(newTable)
                    frm.dashboard.add_section(newTable.outerHTML, "Errors in Cheques")
                },
                error: function(r) {},
                always: function(r) {
                    console.log('in always', r)
                },
                freeze: true,
                freeze_message: "Validating Cheques...",
                async: true,
            });
        })
        // frm.add_custom_button(__('Select Blocked Donor'), function() {
        //     // Fetch all records of the grid
        //     var all_cheque_details = frm.doc.cheque_details;
        //     console.log(all_cheque_details)
        //     var block_donor = [];
        //     console.log(block_donor)
        
        //     // Iterate over each row in the grid
        //     all_cheque_details.forEach(function(row, index) {
        //         // Check if the row meets your condition, for example, if donor_status is "Blocked"
        //         if (row.donor_status == "Blocked") {
        //             // Find the grid row index and click the checkbox
        //             $('*[data-fieldname="cheque_details"]').find('.grid-row-check')[index + 1].click();
        //             block_donor.push(row.donor_status);
        //         }
        //     });
        
        //     frappe.msgprint(__("{0} Rows Selected For Delete", [block_donor.length]));
        // }, __("DELETE"));

        // // $('.primary-action').prop('hidden', true);
        // // frm.add_custom_button(__('Select Blocked Donor'),function(){
        // //         // Iterate over each row in the grid
        // //         var block_donor = []
        // //         $.each(frm.doc.cheque_details, function(index, row) {
        // //             // Check if the row meets your condition, for example, if donor_status is "Blocked"
        // //             if (row.donor_status == "Blocked"){
        // //                 $('*[data-fieldname="cheque_details"]').find('.grid-row-check')[index+1].click()
        // //                 block_donor.push(row.donor_status)    
        // //             }
        // //         });
        // //     frappe.msgprint(__("{0}  Row  Selected  For delete ", [block_donor.length]));
        // // },__("DELETE"));
        // frm.add_custom_button(__('Delete Blocked Donor'),function(){
        //       frappe.confirm('Are you sure you want Delete Row',
        //             () => {
        //                 var grid = frm.fields_dict['cheque_details'].grid;
        //                 var selected_rows = grid.get_selected_children();
        //                 grid.delete_rows(selected_rows)
        //             }, () => {
        //             })  
        // },__("DELETE"));
    $("button[data-original-title=Print]").hide();
    frm.add_custom_button(__('Print Detailed Slip'),function(){
        var cheque_details = frm.doc.cheque_details;
        var current_date = frappe.datetime.now_date();
        frm.set_value("deposit_date",current_date)
        frm.set_value("slip_deposited_status","Yes")
        var block_donor = []
        var all_status_updated = true;
        $.each(cheque_details, function(index, value){
            value.clearing_status = "DEPOSITED";
            if(value.amount == 0){
                frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
                all_status_updated = false;
            }
        });

        var print_format_id = frm.doc.name;
        var formated_url = "/api/method/frappe.utils.print_format.download_pdf?doctype=Slip Form&name=" + print_format_id + "&format=Slip-1&no_letterhead=1&letterhead=No Letterhead&settings={}&_lang=en-US"
        window.open(formated_url);
        frappe.msgprint("Clearing Status DEPOSITED Applied");
        },__("Print"));
    frm.add_custom_button(__('Print Slip '),function(){
        var cheque_details = frm.doc.cheque_details;
        var current_date = frappe.datetime.now_date();
        frm.set_value("deposit_date",current_date)
        frm.set_value("slip_deposited_status","Yes")
        var block_donor = []
        var all_status_updated = true;
        $.each(cheque_details, function(index, value){
            value.clearing_status = "DEPOSITED";
            if(value.amount == 0){
                frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
                var all_status_updated = false;
            }
        });
        var print_format_id = frm.doc.name;
        var formated_url = "/api/method/frappe.utils.print_format.download_pdf?doctype=Slip Form&name=" + print_format_id + "&format=Slip-2&no_letterhead=1&letterhead=No Letterhead&settings={}&_lang=en-US"
        window.open(formated_url);
        frappe.msgprint("Clearing Status DEPOSITED Applied");
        },__("Print"));

    if(frm.doc.name.startsWith("RC")) {
        var button_text = frm.doc.name.startsWith("RC-NB") ? "Return cheques and block donors" : "Return cheques" 
        var freeze_message = frm.doc.name.startsWith("RC-NB") ? "Returning cheques and blocking donors" : "Returning cheques" 
        frm.add_custom_button(__(button_text), function() {
            if(frm.is_dirty()) return frappe.throw("Please save the form!")

            frappe.call({
                method: "ngo.ngo.doctype.slip_form.slip_form.return_cheques_and_block_donors",
                args: {
                    slip_form_name: frm.doc.name
                },
                callback: function(r){
                    frm.refresh()
                },
                freeze: true,
                freeze_message: `${freeze_message}...`
            });
        })
    }

        //// set query on bank account to filter by micr and short code in cheque details child table
        //frm.set_query('account_no', 'cheque_details', function(doc, cdt, cdn) {
        //    var row = frappe.get_doc(cdt, cdn)
        //    return {
        //        filters: {
        //            micr: row.micr_code,
        //            short_account_number: row.short_code
        //        }
        //    }
        //})
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
                // frappe.throw(__("Amount For Check Cannot be Zero For Row Number- ") + value.srno);
            }
        });
        frm.set_value("total_amount_in_slip",total_amount) 
        frm.set_value("number_of_cheques_returned_or_rejected_in_slip",number_of_cheques_returned_or_rejected_in_slip_lst.length)
        frm.set_value("number_of_cheques_deposited_in_slip",totalNumberOfCheckDeposited.length)
        frm.set_value("total_amount_of_deposited_cheques",totalAmountDeposited)
    },
    before_submit: function(frm){
        var cheque_details = frm.doc.cheque_details;
        $.each(cheque_details, function(index, value){
            if (value.clearing_status != "DEPOSITED"){
                frappe.throw(__("Status For Slip Is Not DEPOSITED"));
            }
        });
    },
    cheque_details_on_form_rendered:function(frm,cdt,cdn){
        setupKeyboardShortcuts(frm,cdt,cdn);
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
    account_no: function(frm, cdt, cdn) {
	window.account_no_change_in_cheque_details(frm, cdt, cdn)
    },
    //account_no: window.account_no_change_in_cheque_details,
    // account_no:function(frm,cdt,cdn){
    //     var child = locals[cdt][cdn];
    //     var account_no = child.account_no
    //     if (account_no){

    //          frappe.call({
    //                 method: "ngo.ngo.doctype.slip_form.slip_form.get_donor_details_from_account",
    //                 args: {
    //                     account_no: account_no
    //                 },
    //                 callback: function(r){
                        
    //                     frappe.model.set_value(child.doctype, child.name, "donor_id_number",r.message.name)
    //                     frappe.model.set_value(child.doctype, child.name, "donor_name",r.message.full_name)
    //                     frappe.model.set_value(child.doctype, child.name, "cheque_bank",r.message.bank)
    //                 }
    //             });
    //     }
       
    //     },
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
                    frappe.model.set_value(child.doctype, child.name, "donor_status", r.message.block_status);
                }
            });

        }
    }
   
});

function setupKeyboardShortcuts(frm, cdt, cdn) {
    $(document).off("keydown");
    $(document).keydown(function(e) {
        var cheque_details = cur_frm.doc.cheque_details;
        var child = locals[cdt][cdn];
        var current_row_idx =  cur_frm.open_grid_row().wrapper.find('.grid-form-row-index').text()
        if (e.keyCode === 39) {
              // Display the counter value
            if (current_row_idx < cheque_details.length) {
                // Open the next row in the grid
                cur_frm.open_grid_row().open_next();
            } else {
                frappe.msgprint("All rows have been opened.");
            }
        }
        if (e.keyCode === 37) {
            cur_frm.open_grid_row().open_prev();
        }
    });
}

window.account_no_change_in_cheque_details = function(frm,cdt,cdn,freeze_screen=false){
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
                    frappe.model.set_value(child.doctype, child.name, "cheque_bank",r.message.bank)
                },
                freeze: freeze_screen,
                freeze_message: "Setting donor on basis of account number..."
            });
    }
   
}





  






