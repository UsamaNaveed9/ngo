
frappe.listview_settings['Event Master'] = {
    add_fields: ["status"],
    get_indicator: function(doc) {
        console.log(doc.status);
		var status_color = {
			"Not Started": "black",
			"Started": "green",
			"Extended": "orange",
			"Closed": "red"
		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	}
};
