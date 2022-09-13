// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reconcile', {
	// refresh: function(frm) {

	// }
	get_slip_records: function(frm){
		var t_date = cur_frm.doc.to_date;
		var f_date = cur_frm.doc.from_date;
		frappe.db.get_list('Slip Details', {
			fields: ['name'],
			filters: [["slip_date","between",[f_date,t_date]]]
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
	},
	process:function(frm){
		if(frm.doc.slips.length >= 1 && frm.doc.bank_statement ){
			//console.log(frm.doc.slip, frm.doc.bank_statement);
			var slips_name = [];
			var slips = frm.doc.slips;
			for(var i in slips){
				slips_name.push(slips[i].slip);
			}
			//console.log(slips_name);
				frappe.call({
						method: "ngo.ngo.doctype.reconcile.reconcile.reconcile_fun",
						args: {
								"slips": slips_name,
								"bank_statement": frm.doc.bank_statement
						},
						callback: function(r) {
								if(r.message) {
									//console.log(r.message);
								 	cur_frm.clear_table("reconcile_one");
									for(var i=0;i<r.message.length;i++){
										var childTable = cur_frm.add_child("reconcile_one");
											childTable.cheque_no = r.message[i]["cheque_no"]
											childTable.cheque_date = r.message[i]["cheque_date"]
											childTable.micr_code = r.message[i]["micr_code"]
											childTable.short_code = r.message[i]["short_code"]
											childTable.amount = r.message[i]["amount"]
											childTable.match_value = r.message[i]["match"]
											childTable.match_status = r.message[i]["match_status"]
											childTable.remarks = r.message[i]["remarks"]
											childTable.code = r.message[i]["code"]
											cur_frm.refresh_fields("reconcile_one");
										}

										//cur_frm.save();
								}
						}
				});

		}
	}
});
