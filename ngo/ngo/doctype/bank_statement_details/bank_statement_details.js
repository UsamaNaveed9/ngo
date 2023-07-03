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
	}
	// before_save: function(frm){
	// 	var items = cur_frm.doc.statement_details;
	// 	for(var j in items) {
	// 		if (items[j].cheque_no.length > 6) {
	// 			items[j].cheque_no = items[j].cheque_no.toString().slice(-6);
	// 		} 
	// 		else {
	// 			items[j].cheque_no = String(items[j].cheque_no).padStart(6, '0');
	// 		}
	// 		if (items[j].san.length > 6) {
	// 			items[j].san = items[j].san.toString().slice(-6);
	// 		} 
	// 		else {
	// 			items[j].san = String(items[j].san).padStart(6, '0');
	// 		}
	// 		items[j].code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san+items[j].branch_code+items[j].amount;
	// 		items[j].amount_mis_code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san+items[j].branch_code;
	// 		items[j].micr_mis_code = ''+items[j].cheque_date+items[j].cheque_no+items[j].san+items[j].branch_code+items[j].amount;
	// 		items[j].cheque_no_mis_code = ''+items[j].cheque_date+items[j].micr+items[j].san+items[j].branch_code+items[j].amount;
	// 		items[j].san_mis_code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].branch_code+items[j].amount;
	// 		//items[j].code = ''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san;
	// 		//console.log(''+items[j].cheque_date+items[j].cheque_no+items[j].micr+items[j].san);
	// 	}
	// }
});
