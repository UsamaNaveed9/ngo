// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bank Statement Details', {
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
	before_save: function(frm){
		var items = cur_frm.doc.statement_details;
		for(var j in items) {
			items[j].code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san+items[j].amount;
			//items[j].code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san;
			//console.log(''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san);
		}
	}
});
