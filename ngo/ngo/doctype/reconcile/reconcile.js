// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reconcile', {
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
	},
	refresh: function(frm) {
		frm.set_query('bank_statement', function(doc) {
			return {
				filters: {
					'bank_account': frm.doc.bank_account,
				}
			}
		});
	},
	get_slip_records: function(frm){
		var t_date = cur_frm.doc.to_date;
		var f_date = cur_frm.doc.from_date;
		var bank = cur_frm.doc.bank_account;
		frappe.db.get_list('Slip Details', {
			fields: ['name'],
			filters:[
						["slip_date","between",[f_date,t_date]],
						["deposit_account","=",bank]
					]
		}).then(records => {
			//console.log(records,records.length);
			if(records.length >=1 ){
				cur_frm.clear_table("slips");
				for(var i=0;i<records.length;i++){
					var add = cur_frm.add_child("slips");
					add.slip = records[i]["name"]
					cur_frm.refresh_fields("slips");
				}
			}
			else{
				frappe.msgprint(__('No records exist between these dates'));
			}
		})
	}
	// process:function(frm){
	// 	if(frm.doc.slips.length >= 1 && frm.doc.bank_statement ){
	// 		//console.log(frm.doc.slip, frm.doc.bank_statement);
	// 		var slips_name = [];
	// 		var slips = frm.doc.slips;
	// 		for(var i in slips){
	// 			slips_name.push(slips[i].slip);
	// 		}
	// 		//console.log(slips_name);
	// 			frappe.call({
	// 					method: "ngo.ngo.doctype.reconcile.reconcile.reconcile_fun",
	// 					args: {
	// 							"slips": slips_name,
	// 							"bank_statement": frm.doc.bank_statement
	// 					},
	// 					freeze: true,
    // 					freeze_message: "Processing",
	// 					callback: function(r) {
	// 							if(r.message) {
	// 								//console.log(r.message);
	// 							 	cur_frm.clear_table("reconcile_one");
	// 								for(var i=0;i<r.message.length;i++){
	// 									var childTable = cur_frm.add_child("reconcile_one");
	// 										childTable.cheque_no = r.message[i]["cheque_no"]
	// 										childTable.cheque_date = r.message[i]["cheque_date"]
	// 										childTable.micr_code = r.message[i]["micr_code"]
	// 										childTable.short_code = r.message[i]["short_code"]
	// 										childTable.amount = r.message[i]["amount"]
	// 										childTable.match_value = r.message[i]["match"]
	// 										childTable.match_status = r.message[i]["match_status"]
	// 										childTable.not_matching_fields = r.message[i]["not_matching_fields"]
	// 										childTable.values = r.message[i]["values"]
	// 										childTable.main_from = r.message[i]["main_from"]
	// 										childTable.code = r.message[i]["code"]
	// 										childTable.checked_code = r.message[i]["checked_code"]
	// 										cur_frm.refresh_fields("reconcile_one");
	// 									}

	// 									//cur_frm.save();
	// 							}
	// 					}
	// 			});

	// 	}
	// }
});