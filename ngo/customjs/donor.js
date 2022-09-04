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
		})
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
