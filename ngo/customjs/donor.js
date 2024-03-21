frappe.ui.form.on('Donor', {
	setup: function(frm) {
	    var country = cur_frm.doc.country; 
		frm.set_query("region", function() {
			return {
				filters: [
					["Territory","parent_territory", "in", country]
				]
			}
		});

		frm.set_query('customer_primary_address', function(doc) {
			return {
				filters: {
					'link_doctype': 'Donor',
					'link_name': doc.name
				}
			}
		});

		frm.fields_dict['account'].grid.get_field("bank_account").get_query = function(doc, cdt, cdn) {
			return {
				filters: [
					['Bank Account', 'donor_id', '=', frm.doc.name ],
					
				]
			}
		}
	},
	country: function(frm){
	    var country = cur_frm.doc.country;
	    frm.set_query("region", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", country ]        
	            ]
	        }
	    })
	},
	region: function(frm){
	    var region = cur_frm.doc.region;
	    frm.set_query("state", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", region ]        
	            ]
	        }
	    })
	},
	state: function(frm){
	    var state = cur_frm.doc.state;
	    frm.set_query("district", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", state ]        
	            ]
	        }
	    })
	},
    district: function(frm){
	    var dist = cur_frm.doc.district;
	    frm.set_query("zone", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", dist ]        
	            ]
	        }
	    })
	},
	zone: function(frm){
	    var zone = cur_frm.doc.zone;
	    frm.set_query("locality", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", zone ]        
	            ]
	        }
	    })
	},
	
	electronic_trans_limit: function(frm){
		var ch_l = frm.doc.cheque_trans_limit;
		var elect_l = frm.doc.electronic_trans_limit;
		if(elect_l > ch_l){
			frappe.throw(__('Electronic Limit greater than Cheque Limit'))
		}
	},
	pan_number: function(frm){
		if (frm.doc.pan_number.length < 10 || frm.doc.pan_number.length > 10 ){
            frappe.throw(__('Enter a valid PAN Number'))
        }
		if ( cur_frm.doc.donor_type == "Individual"){
			if (frm.doc.pan_number[3] != "P"){
				frappe.throw(__('Donor Type Individual, The 4th character of PAN Number must be "P"'))
			}
		}
	},
	aadhar: function(frm){
		if (frm.doc.aadhar.length > 12 ){
            frappe.throw(__('Enter a valid Aadhar'))
        }
	}

});

frappe.ui.form.on('Donor Bank detail', {
    bank_account: function(frm, cdt, cdn){
        var child_doc = locals[cdt][cdn];
        frappe.call({
            method: "ngo.custome_py.donar.get_data_from_bank_donar_details",
            args: {
                donar_id: frm.doc.name,
                account_number: child_doc.bank_account
            },
            callback: function(r){
                if(r.message){
                    var bank_details = r.message;
                    $.each(bank_details, function(i, v){
                        // Set values for fields in the parent form using cur_frm
                        frappe.model.set_value(cdt, cdn, 'micr_code', v.micr);
                        frappe.model.set_value(cdt, cdn, 'branch_code', v.branch_code);
                        frappe.model.set_value(cdt, cdn, "bank", v.bank);
                        frappe.model.set_value(cdt, cdn, "short_account_number",v.short_account_number);
                    
                    });
                    cur_frm.refresh_field("account");
                } 
            }
        });
    },
});


