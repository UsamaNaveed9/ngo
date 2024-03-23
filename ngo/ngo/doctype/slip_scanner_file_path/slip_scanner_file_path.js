// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Scanner File Path',{
	refresh: function(frm){
	frm.set_query('bank_accounts',function(doc){
		return {
			filters:{
				"is_company_account":1,
				}
			};
		});
		
		frm.trigger("get_todays_date")	

	},
	
	upload:function(frm){
		frappe.call({
					method: "ngo.ngo.doctype.slip_scanner_file_path.slip_scanner_file_path.read_csv",
					args: {
						file: frm.doc.slip_scanner_file_path,
					},
					freeze:true,
					freeze_message:"Record Creation is Started. Please Wait......",
					callback:function(r){
						 {
							var message = r.message + " " +'Slip Created';
							var timeout = 5; 
							frappe.show_alert(message, timeout);
						}
					}
				});
			},

	get_todays_date:function(frm){
		var today = new Date();
		// Get the current date
		var day = today.getDate();
		var month = today.getMonth() + 1; // Months are zero-based, so we add 1
		var year = today.getFullYear();
		var formattedDate = year + "-" + (month < 10 ? "0" + month : month) + "-" + (day < 10 ? "0" + day : day);

		frm.set_value("deposit_date",formattedDate)
		// var formattedDate = today.toISOString().slice(0,10);

	}
		

		});

	







