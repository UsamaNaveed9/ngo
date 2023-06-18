// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Details', {
	setup: function(frm) {
		frm.set_query("deposit_account", function(){
		    return {
		        filters: [
		            ["Bank Account","is_company_account","=", "1"]
		        ]
		    }
		});
	},
	before_save: function(frm){
		var items = cur_frm.doc.cheque_details;
		for(var j in items) {
			if (items[j].cheque_number.length > 6) {
				items[j].cheque_number = items[j].cheque_number.toString().slice(-6);
			} 
			else {
				items[j].cheque_number = String(items[j].cheque_number).padStart(6, '0');
			}
			if (items[j].short_code.length > 6) {
				items[j].short_code = items[j].short_code.toString().slice(-6);
			} 
			else {
				items[j].short_code = String(items[j].short_code).padStart(6, '0');
			}
			items[j].code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code+items[j].branch_code+items[j].amount;
			items[j].amount_mis_code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code+items[j].branch_code;
			items[j].micr_mis_code = ''+items[j].cheque_date+items[j].cheque_number+items[j].short_code+items[j].branch_code+items[j].amount;
			items[j].cheque_no_mis_code = ''+items[j].cheque_date+items[j].micr_code+items[j].short_code+items[j].branch_code+items[j].amount;
			items[j].san_miss_code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].branch_code+items[j].amount;
			//items[j].code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code;
			//console.log(''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code);
			//items[j].image = '/'+items[j].event+'/'+items[j].token+'_'+items[j].srno+'_ChequeImage.jpg'
		}

	}
});
