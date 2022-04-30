frappe.ui.form.on('Donor', {
	electronic_trans_limit: function(frm){
		var total = frm.doc.total_limit;
		var electronic = frm.doc.electronic_trans_limit;
		frm.set_value("cheque_trans_limit", total - electronic);
		frm.refresh_field('cheque_trans_limit');
	}
});