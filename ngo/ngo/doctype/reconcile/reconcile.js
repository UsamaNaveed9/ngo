// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reconcile', {
	// refresh: function(frm) {

	// }
	process:function(frm){
		if(frm.doc.slip && frm.doc.bank_statement ){
			//console.log(frm.doc.slip, frm.doc.bank_statement);
				frappe.call({
						method: "ngo.ngo.doctype.reconcile.reconcile.reconcile_fun",
						args: {
								"slip": frm.doc.slip,
								"bank_statement": frm.doc.bank_statement
						},
						callback: function(r) {
								if(r.message) {
									//console.log(r.message);
								 	cur_frm.clear_table("reconcile_detail");
									for(var i=0;i<r.message.length;i++){
										var childTable = cur_frm.add_child("reconcile_detail");
											childTable.cheque_no = r.message[i]["cheque_no"]
											childTable.cheque_date = r.message[i]["cheque_date"]
											childTable.account_no = r.message[i]["account_no"]
											childTable.micr_code = r.message[i]["micr_code"]
											childTable.short_code = r.message[i]["short_code"]
											childTable.amount = r.message[i]["amount"]
											childTable.match = r.message[i]["match"]
											childTable.match_status = r.message[i]["match_status"]
											cur_frm.refresh_fields("reconcile_detail");
										}

										cur_frm.save();
								}
						}
				});

		}
	}
});
