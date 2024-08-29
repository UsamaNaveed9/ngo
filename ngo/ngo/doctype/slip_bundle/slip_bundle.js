// Copyright (c) 2024, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Bundle', {
	refresh: function(frm) {
		frm.set_query('deposit_account', () => {
			return {
				filters: {
					is_company_account: true
				}
			}
		})

		frm.set_query('slip_form', 'items', (frm) => {
			return {
				filters: {
					slip_event_code: frm.slip_bundle_event_code,
					deposit_account: frm.deposit_account,
					name: ['NOT LIKE', 'DT%']
				}
			}
		})

		frm.add_custom_button(__("Validate"), function() {
			if(frm.is_dirty()) return frappe.throw("Please save the form!")

			frappe.call({
				method: "ngo.ngo.doctype.slip_bundle.slip_bundle.validate_slip_bundle",
				args: {
					slip_bundle_name: frm.doc.name
				},
				callback: function(r){
					frm.refresh()
				},
				freeze: true,
				freeze_message: "Validating Slips..."
			});
		})
	}
});

frappe.ui.form.on('Slip Bundle Item', {
	slip_form: function(frm) {
		console.log('set hua')
	}
});
