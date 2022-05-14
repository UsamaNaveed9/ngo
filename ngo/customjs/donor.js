frappe.ui.form.on('Donor', {
	before_save: function(frm){
		var ch_l = frm.doc.cheque_trans_limit;
		var elect_l = frm.doc.electronic_trans_limit;
		if(elect_l > ch_l){
			frappe.msgprint(
				msg='Electronic Limit greater than Cheque Limit',
				title='Error',
				raise_exception=FileNotFoundError
			)
		}
	},
	electronic_trans_limit: function(frm){
		var ch_l = frm.doc.cheque_trans_limit;
		var elect_l = frm.doc.electronic_trans_limit;
		if(elect_l > ch_l){
			frappe.msgprint(
				msg='Electronic Limit greater than Cheque Limit',
				title='Error',
				raise_exception=FileNotFoundError
			)
		}
	}
});
