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
			items[j].code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code+items[j].amount;
			//items[j].code = ''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code;
			//console.log(''+items[j].cheque_date+items[j].cheque_number+items[j].micr_code+items[j].short_code);
			items[j].image = '/'+items[j].event+'/'+items[j].token+'_'+items[j].srno+'_ChequeImage.jpg'
		}

	}
});
