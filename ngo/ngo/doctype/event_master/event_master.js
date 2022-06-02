// Copyright (c) 2022, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event Master', {
	before_save: function(frm){
		if(frm.doc.extend_ends_on){
			if(frm.doc.ends_on){
				frm.set_value('status', 'Extended');
			}
		}
	},
	setup: function(frm) {
	    var country = cur_frm.doc.country; 
		frm.set_query("region", function() {
			return {
				filters: [
					["Territory","parent_territory", "in", country]
				]
			}
		});
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
	    frm.set_query("centre", function(){
	        return {
	            filters: [
	                ["Territory","parent_territory", "=", zone ]        
	            ]
	        }
	    })
	},
	get_participants: function(frm){
		let e_status = frm.doc.donor_status;
		let a_status = frm.doc.active_status;
		let country = frm.doc.country;
		let region = frm.doc.region;
		let state = frm.doc.state;
		let district = frm.doc.district;
		let zone = frm.doc.zone;
		let centre = frm.doc.centre;
		
		frappe.db.get_list('Donor', {
			fields: ['name','donor_name','last_name','locality'],
			filters: {
				status: e_status,
				active_status: a_status,
				country: country,
				region: region,
				state: state,
				district: district,
				zone: zone,
				locality: centre
			}
		}).then(records => {
			cur_frm.clear_table("event_participants");
			for(var rec in records){
				//console.log(records[rec].name);  
        		var dnr = cur_frm.add_child("event_participants");
        		dnr.donor_id = records[rec].name;
				dnr.donor_name = records[rec].donor_name + " " + records[rec].last_name;
				dnr.centre = records[rec].locality;
			}
			cur_frm.refresh_fields("event_participants");
		})
	}
});
