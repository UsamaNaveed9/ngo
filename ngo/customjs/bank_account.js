frappe.ui.form.on('Bank Account', {
	bank(frm) {
		var bank = frm.doc.bank;
		frm.set_query("ifsc", function() {
    		return {
				filters: [
					["IFSC","bank_name", "in", bank]
				]
			}
		});
	}
})