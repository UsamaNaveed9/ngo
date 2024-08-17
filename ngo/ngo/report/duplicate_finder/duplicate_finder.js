// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Duplicate Finder"] = {
	"filters": [
		{
			fieldname: 'event',
			label: __('Event'),
			fieldtype: 'Link',
			options: 'Event Master',
			on_change: function() {
				frappe.query_report.set_filter_value('slip_forms', [])
			}
		},
		{
			"fieldname": "slip_forms",
			"label": __("Slip Forms"),
			"fieldtype": "MultiSelectList",
			"get_data": function(txt) {
				var filters = {}
				if(frappe.query_report.get_filter_value('event').length > 0) {
					filters['slip_event_code'] = frappe.query_report.get_filter_value('event')
				}
				return frappe.db.get_link_options("Slip Form", txt, filters);
			}
		}
	]
};
