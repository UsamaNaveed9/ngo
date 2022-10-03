// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Reconcile', {
	refresh(frm) {
		$(".grid-add-row").hide();
	},
	select_event(frm){
		if(cur_frm.doc.select_event){
			frm.save();
		}
	},
	get_data: function(frm){
		frm.set_value("index", 0)
		frm.set_value("record", cur_frm.doc.index + 1)
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
								childTable.checked_code = r.message[i]["checked_code"]
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
								childTable.checked_code = r.message[i]["checked_code"]
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
				if(cur_frm.doc.code[cur_frm.doc.index].checked_code){
					frappe.call({
						method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
						args: {
								"slips": slips_name,
								"checked_code": cur_frm.doc.code[cur_frm.doc.index].checked_code
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
				}
				

				var bs_name = doc.bank_statement;
				if(cur_frm.doc.code[cur_frm.doc.index].code){
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

				}
				

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
    		});
	},
	previous: function(frm){
		cur_frm.clear_table("slip");
		cur_frm.clear_table("bank_statement");
		frm.set_value("index", cur_frm.doc.index - 1);
		frm.set_value("record", cur_frm.doc.record - 1);
		let idx = cur_frm.doc.record;
		if (idx<1){
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
				if(cur_frm.doc.code[cur_frm.doc.index].checked_code){
					frappe.call({
						method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
						args: {
								"slips": slips_name,
								"checked_code": cur_frm.doc.code[cur_frm.doc.index].checked_code
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
				}

				var bs_name = doc.bank_statement;
				if(cur_frm.doc.code[cur_frm.doc.index].code){
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
				}
				

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
		cur_frm.clear_table("slip");
		cur_frm.clear_table("bank_statement");
		frm.set_value("index", cur_frm.doc.index + 1);
		frm.set_value("record", cur_frm.doc.record + 1);
		let idx = cur_frm.doc.record;
		if (idx>cur_frm.doc.total_records){
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

				if(cur_frm.doc.code[cur_frm.doc.index].checked_code){
					frappe.call({
						method: "ngo.ngo.doctype.manual_reconcile.manual_reconcile.get_slip_record",
						args: {
								"slips": slips_name,
								"checked_code": cur_frm.doc.code[cur_frm.doc.index].checked_code
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
				}
				

				var bs_name = doc.bank_statement;
				if(cur_frm.doc.code[cur_frm.doc.index].code){
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
				}

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
	done: function(frm){
		let count = 0;
		let idx = 0;

		for(var i=0; i<cur_frm.doc.records.length; i++){
			if(cur_frm.doc.code[cur_frm.doc.index].code && cur_frm.doc.records[i].id == cur_frm.doc.code[cur_frm.doc.index].code ){
				count = 1;
				idx = i;
			}
			else if(cur_frm.doc.records[i].id == cur_frm.doc.code[cur_frm.doc.index].checked_code ){
				count = 1;
				idx = i;
			}
		}	
		
		if(count == 1){
			if(cur_frm.doc.code[cur_frm.doc.index].code){
				cur_frm.doc.records[idx].id = cur_frm.doc.code[cur_frm.doc.index].code
			}
			else{
				cur_frm.doc.records[idx].id = cur_frm.doc.code[cur_frm.doc.index].checked_code
			}
			cur_frm.doc.records[idx].reconcile_status = cur_frm.doc.reconcile_status
			cur_frm.doc.records[idx].note_or_proof = cur_frm.doc.note_or_proof
			cur_frm.doc.records[idx].remarks = cur_frm.doc.remarks
			cur_frm.refresh_fields("records");
		}
		else{
			var rec = cur_frm.add_child("records");
			if(cur_frm.doc.code[cur_frm.doc.index].code){
				rec.id = cur_frm.doc.code[cur_frm.doc.index].code
			}
			else{
				rec.id = cur_frm.doc.code[cur_frm.doc.index].checked_code
			}
			rec.reconcile_status = cur_frm.doc.reconcile_status
			rec.note_or_proof = cur_frm.doc.note_or_proof
			rec.remarks = cur_frm.doc.remarks
			cur_frm.refresh_fields("records");
		}
		cur_frm.set_value("note_or_proof","");
		cur_frm.refresh_fields("note_or_proof");
		cur_frm.set_value("remarks","");
		cur_frm.refresh_fields("remarks");
	}
});
