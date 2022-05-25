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
	before_save: function(frm){
		var ch_l = frm.doc.cheque_trans_limit;
		var elect_l = frm.doc.electronic_trans_limit;
		if(elect_l > ch_l){
			frappe.throw(__('Electronic Limit greater than Cheque Limit'))
		}
	},
	electronic_trans_limit: function(frm){
		var ch_l = frm.doc.cheque_trans_limit;
		var elect_l = frm.doc.electronic_trans_limit;
		if(elect_l > ch_l){
			frappe.throw(__('Electronic Limit greater than Cheque Limit'))
		}
	}
});
