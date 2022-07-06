// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Reconcile', {
	get_data(frm){
		frm.set_value("index", 0)
		fram.refresh()
	},
	previous(frm){
		let idx = frm.doc.index;
		idx = idx -1;
		if (idx<0){
			frappe.throw("No Data")
		}
		let short_code = frm.doc.account[idx].account
		frm.set_value("index", idx)
		console.log(idx)
		console.log(short_code)
		frm.save()
	}
});
