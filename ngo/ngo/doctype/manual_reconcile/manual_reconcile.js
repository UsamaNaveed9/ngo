// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Reconcile', {
	get_data: function(frm){
		frm.set_value("index", 0)
		if(cur_frm.doc.reconcile && cur_frm.doc.match_status != "All Records"){
			frappe.call({
				method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.reconcile_fun",
				args: {
						"rec": frm.doc.reconcile,
						"status": frm.doc.match_status
				},
				callback: function(r) {
						if(r.message) {
							//console.log(r.message);
							frm.set_value("total_records", r.message.length);
							cur_frm.clear_table("code");
							for(var i=0;i<r.message.length;i++){
								var childTable = cur_frm.add_child("code");
								childTable.code = r.message[i]["code"]
								cur_frm.refresh_fields("code");
							}
						}
					}
				})
		}
		else if(cur_frm.doc.reconcile && cur_frm.doc.match_status == "All Records"){
			frappe.call({
				method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.reconcile_funAll",
				args: {
						"rec": frm.doc.reconcile,
				},
				callback: function(r) {
						if(r.message) {
							//console.log(r.message);
							frm.set_value("total_records", r.message.length);
							cur_frm.clear_table("code");
							for(var i=0;i<r.message.length;i++){
								var childTable = cur_frm.add_child("code");
								childTable.code = r.message[i]["code"]
								cur_frm.refresh_fields("code");
							}
						}
					}
				})
		}
		frappe.db.get_doc('Reconcile', frm.doc.reconcile)
    		.then(doc => {
        		//console.log(doc.slips)
				var slips_name = [];
				var slips = doc.slips;
				for(var i in slips){
					slips_name.push(slips[i].slip);
				}
				//console.log(slips_name);
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
					args: {
							"slips": slips_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
							if(r.message) {
								//console.log(r.message[0]);
								var slip_r = r.message[0];
									cur_frm.clear_table("slip");
									for(var i=0;i<slip_r.length;i++){
										var childTable = cur_frm.add_child("slip");
										childTable.cheque_no = slip_r[i]["cheque_number"]
										childTable.cheque_date = slip_r[i]["cheque_date"]
										childTable.account_no = slip_r[i]["account_no"]
										childTable.micr_code = slip_r[i]["micr_code"]
										childTable.short_code = slip_r[i]["short_code"]
										childTable.amount = slip_r[i]["amount"]
										childTable.image_path = slip_r[i]["image"]
										var path = slip_r[i]["image"]
										cur_frm.refresh_fields("slip");
									}

								var wrapper = frm.get_field("preview_html").$wrapper;
								
								frm.toggle_display("preview", path);
								frm.toggle_display("preview_html", path);
								
								if(path){
									wrapper.html('<div class="img_preview">\
										<img class="img-responsive" src="'+path+'"></img>\
										</div>');
								} else {
									wrapper.empty();
								}	
							}
						}
					})

				var bs_name = doc.bank_statement;
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_bs_record",
					args: {
							"bs_name": bs_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
							if(r.message) {
								//console.log(r.message);
									cur_frm.clear_table("bank_statement");
									for(var i=0;i<r.message.length;i++){
										var childTable = cur_frm.add_child("bank_statement");
										childTable.cheque_no = r.message[i]["cheque_no"]
										childTable.cheque_date = r.message[i]["cheque_date"]
										childTable.account_no = r.message[i]["account_no"]
										childTable.micr_code = r.message[i]["micr"]
										childTable.short_code = r.message[i]["san"]
										childTable.amount = r.message[i]["amount"]
										cur_frm.refresh_fields("bank_statement");
									}
							}
						}
					})

					// frappe.call({
					// 	method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_re_record",
					// 	args: {
					// 			"re_name": frm.doc.reconcile,
					// 			"code": cur_frm.doc.code[cur_frm.doc.index].code
					// 	},
					// 	callback: function(r) {
					// 			if(r.message) {
					// 				//console.log(r.message);
					// 					cur_frm.clear_table("reconcile_details");
					// 					for(var i=0;i<r.message.length;i++){
					// 						var childTable = cur_frm.add_child("reconcile_details");
					// 						childTable.cheque_no = r.message[i]["cheque_no"]
					// 						childTable.cheque_date = r.message[i]["cheque_date"]
					// 						childTable.account_no = r.message[i]["account_no"]
					// 						childTable.micr_code = r.message[i]["micr_code"]
					// 						childTable.short_code = r.message[i]["short_code"]
					// 						childTable.amount = r.message[i]["amount"]
					// 						childTable.match_value = r.message[i]["match_value"]
					// 						childTable.match_status = r.message[i]["match_status"]
					// 						cur_frm.refresh_fields("reconcile_details");
					// 					}
					// 			}
					// 		}
					// 	})
					
    		})	
			
	},
	previous: function(frm){
		frm.set_value("index", cur_frm.doc.index - 1);
		let idx = cur_frm.doc.index;
		if (idx<0){
			frappe.throw("No Data")
		}
		else{
			frappe.db.get_doc('Reconcile', frm.doc.reconcile)
    		.then(doc => {
        		//console.log(doc.slips)
				var slips_name = [];
				var slips = doc.slips;
				for(var i in slips){
					slips_name.push(slips[i].slip);
				}
				//console.log(slips_name);
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
					args: {
							"slips": slips_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
						if(r.message) {
							//console.log(r.message[0]);
							var slip_r = r.message[0];
								cur_frm.clear_table("slip");
								for(var i=0;i<slip_r.length;i++){
									var childTable = cur_frm.add_child("slip");
									childTable.cheque_no = slip_r[i]["cheque_number"]
									childTable.cheque_date = slip_r[i]["cheque_date"]
									childTable.account_no = slip_r[i]["account_no"]
									childTable.micr_code = slip_r[i]["micr_code"]
									childTable.short_code = slip_r[i]["short_code"]
									childTable.amount = slip_r[i]["amount"]
									childTable.image_path = slip_r[i]["image"]
									var path = slip_r[i]["image"]
									cur_frm.refresh_fields("slip");
								}

							var wrapper = frm.get_field("preview_html").$wrapper;
							
							frm.toggle_display("preview", path);
							frm.toggle_display("preview_html", path);
							
							if(path){
								wrapper.html('<div class="img_preview">\
									<img class="img-responsive" src="'+path+'"></img>\
									</div>');
							} else {
								wrapper.empty();
							}	
						}
						}
					})

				var bs_name = doc.bank_statement;
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_bs_record",
					args: {
							"bs_name": bs_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
							if(r.message) {
								//console.log(r.message);
									cur_frm.clear_table("bank_statement");
									for(var i=0;i<r.message.length;i++){
										var childTable = cur_frm.add_child("bank_statement");
										childTable.cheque_no = r.message[i]["cheque_no"]
										childTable.cheque_date = r.message[i]["cheque_date"]
										childTable.account_no = r.message[i]["account_no"]
										childTable.micr_code = r.message[i]["micr"]
										childTable.short_code = r.message[i]["san"]
										childTable.amount = r.message[i]["amount"]
										cur_frm.refresh_fields("bank_statement");
									}
							}
						}
					})

					// frappe.call({
					// 	method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_re_record",
					// 	args: {
					// 			"re_name": frm.doc.reconcile,
					// 			"code": cur_frm.doc.code[cur_frm.doc.index].code
					// 	},
					// 	callback: function(r) {
					// 			if(r.message) {
					// 				//console.log(r.message);
					// 					cur_frm.clear_table("reconcile_details");
					// 					for(var i=0;i<r.message.length;i++){
					// 						var childTable = cur_frm.add_child("reconcile_details");
					// 						childTable.cheque_no = r.message[i]["cheque_no"]
					// 						childTable.cheque_date = r.message[i]["cheque_date"]
					// 						childTable.account_no = r.message[i]["account_no"]
					// 						childTable.micr_code = r.message[i]["micr_code"]
					// 						childTable.short_code = r.message[i]["short_code"]
					// 						childTable.amount = r.message[i]["amount"]
					// 						childTable.match_value = r.message[i]["match_value"]
					// 						childTable.match_status = r.message[i]["match_status"]
					// 						cur_frm.refresh_fields("reconcile_details");
					// 					}
					// 			}
					// 		}
					// 	})
    		})
		}
	},
	next: function(frm){
		frm.set_value("index", cur_frm.doc.index + 1);
		let idx = cur_frm.doc.index;
		if (idx>cur_frm.doc.code.length){
			frappe.throw("No Data")
		}
		else{
			frappe.db.get_doc('Reconcile', frm.doc.reconcile)
    		.then(doc => {
        		//console.log(doc.slips)
				var slips_name = [];
				var slips = doc.slips;
				for(var i in slips){
					slips_name.push(slips[i].slip);
				}
				//console.log(slips_name);
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
					args: {
							"slips": slips_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
						if(r.message) {
							//console.log(r.message[0]);
							var slip_r = r.message[0];
								cur_frm.clear_table("slip");
								for(var i=0;i<slip_r.length;i++){
									var childTable = cur_frm.add_child("slip");
									childTable.cheque_no = slip_r[i]["cheque_number"]
									childTable.cheque_date = slip_r[i]["cheque_date"]
									childTable.account_no = slip_r[i]["account_no"]
									childTable.micr_code = slip_r[i]["micr_code"]
									childTable.short_code = slip_r[i]["short_code"]
									childTable.amount = slip_r[i]["amount"]
									childTable.image_path = slip_r[i]["image"]
									var path = slip_r[i]["image"]
									cur_frm.refresh_fields("slip");
								}

							var wrapper = frm.get_field("preview_html").$wrapper;
							
							frm.toggle_display("preview", path);
							frm.toggle_display("preview_html", path);
							
							if(path){
								wrapper.html('<div class="img_preview">\
									<img class="img-responsive" src="'+path+'"></img>\
									</div>');
							} else {
								wrapper.empty();
							}	
						}
						}
					})

				var bs_name = doc.bank_statement;
				frappe.call({
					method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_bs_record",
					args: {
							"bs_name": bs_name,
							"code": cur_frm.doc.code[cur_frm.doc.index].code
					},
					callback: function(r) {
							if(r.message) {
								//console.log(r.message);
									cur_frm.clear_table("bank_statement");
									for(var i=0;i<r.message.length;i++){
										var childTable = cur_frm.add_child("bank_statement");
										childTable.cheque_no = r.message[i]["cheque_no"]
										childTable.cheque_date = r.message[i]["cheque_date"]
										childTable.account_no = r.message[i]["account_no"]
										childTable.micr_code = r.message[i]["micr"]
										childTable.short_code = r.message[i]["san"]
										childTable.amount = r.message[i]["amount"]
										cur_frm.refresh_fields("bank_statement");
									}
							}
						}
					})

					// frappe.call({
					// 	method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_re_record",
					// 	args: {
					// 			"re_name": frm.doc.reconcile,
					// 			"code": cur_frm.doc.code[cur_frm.doc.index].code
					// 	},
					// 	callback: function(r) {
					// 			if(r.message) {
					// 				//console.log(r.message);
					// 					cur_frm.clear_table("reconcile_details");
					// 					for(var i=0;i<r.message.length;i++){
					// 						var childTable = cur_frm.add_child("reconcile_details");
					// 						childTable.cheque_no = r.message[i]["cheque_no"]
					// 						childTable.cheque_date = r.message[i]["cheque_date"]
					// 						childTable.account_no = r.message[i]["account_no"]
					// 						childTable.micr_code = r.message[i]["micr_code"]
					// 						childTable.short_code = r.message[i]["short_code"]
					// 						childTable.amount = r.message[i]["amount"]
					// 						childTable.match_value = r.message[i]["match_value"]
					// 						childTable.match_status = r.message[i]["match_status"]
					// 						cur_frm.refresh_fields("reconcile_details");
					// 					}
					// 			}
					// 		}
					// 	})
    		})
		}
	}
});
