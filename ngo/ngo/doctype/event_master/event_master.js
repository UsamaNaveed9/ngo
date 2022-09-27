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
		if(cur_frm.doc.country){
			var country = cur_frm.doc.country; 
			frm.set_query("region", function() {
				return {
					filters: [
						["Territory","parent_territory", "in", country]
					]
				}
			});
		}
		if(cur_frm.doc.country){
	    	var country = cur_frm.doc.country;
	    	frm.set_query("region", function(){
	        	return {
	            	filters: [
	                	["Territory","parent_territory", "=", country ]        
	            	]
	        	}
	    	});
		}	
	},
	country: function(frm){
		if(cur_frm.doc.country){
	    	var country = cur_frm.doc.country;
	    	frm.set_query("region", function(){
	        	return {
	            	filters: [
	                	["Territory","parent_territory", "=", country ]        
	            	]
	        	}
	    	});
		}
	},
	region: function(frm){
		if(cur_frm.doc.region){
			var region = cur_frm.doc.region;
	    	frm.set_query("state", function(){
	        	return {
	            	filters: [
	                	["Territory","parent_territory", "=", region ]        
	            	]
	        	}
	   		});
		}   
	},
	state: function(frm){
		if(cur_frm.doc.state){
			var state = cur_frm.doc.state;
	    	frm.set_query("district", function(){
	        	return {
	            	filters: [
	                	["Territory","parent_territory", "=", state ]        
	            	]
	        	}
	    	});
		} 
	},
    district: function(frm){
		if(cur_frm.doc.district){
			var dist = cur_frm.doc.district;
	    	frm.set_query("zone", function(){
	       		return {
	            	filters: [
	                	["Territory","parent_territory", "=", dist ]        
	            	]
	        	}
	    	});	
		} 
	},
	zone: function(frm){
		if(cur_frm.doc.zone){
			var zone = cur_frm.doc.zone;
	    	frm.set_query("centre", function(){
	        	return {
	            	filters: [
	                	["Territory","parent_territory", "=", zone ]        
	            	]
	        	}
	    	});
		}    
	},
	get_participants: function(frm){
		var d = {}
		if(frm.doc.donor_status){
			d["status"] = frm.doc.donor_status
		}
		if(frm.doc.active_status){
			d["active_status"] = frm.doc.active_status
		}
		if(frm.doc.country){
			d["country"] = frm.doc.country
		}
		if(frm.doc.region){
			d["region"] = frm.doc.region
		}
		if(frm.doc.state){
			d["state"] = frm.doc.state
		}
		if(frm.doc.district){
			d["district"] = frm.doc.district
		}
		if(frm.doc.zone){
			d["zone"] = frm.doc.zone
		}
		if(frm.doc.centre){
			d["locality"] = frm.doc.centre
		}

		//console.log(d)
		
		frappe.db.get_list('Donor', {
			fields: ['name','donor_name','last_name','locality'],
			filters: d,
			limit: 10000,
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
