frappe.listview_settings['Slip Form'] = {
    onload:function(listview) {
        // Filter the list vie columns to exclude columns with type 'Status'
        listview.columns = listview.columns.filter(column => {
            return column.type !== 'Status';
        });
    }
};