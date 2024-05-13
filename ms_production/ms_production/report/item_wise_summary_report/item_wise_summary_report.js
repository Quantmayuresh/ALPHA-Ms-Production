// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Wise Summary Report"] = {
    "filters": [
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
            "reqd": 0,
        },
        {
            "label": "From Date",
            "fieldname": "f_date",
            "fieldtype": "Date",
            "width": 200,
            "reqd": 0,
        },
        {
            "label": "To Date", 
            "fieldname": "t_date", 
            "fieldtype": "Date",
            "reqd": 0,
            
        },
        {
            "label": "Supervisor",
            "fieldname": "supervisor",
            "fieldtype": "Link",
            "options": "Supervisor Master",
        },
        {
            "label": "Operator",
            "fieldname": "operator",
            "fieldtype": "Link",
            "options": "Operator Master",
        },
        {
            "label": "Shift",
            "fieldname": "shift",
            "fieldtype": "Link",
            "options": "Shift Time",
        },
        {
            "label": "Finished Item",
            "fieldname": "finished_item",
            "fieldtype": "Link",
            "options": "Item",
        },
        // {
        //     "label": "Warehouse",
        //     "fieldname": "warehouse",
        //     "fieldtype": "Link",
        //     "options": "Warehouse",
        // },
        {
            "label": "Machine",
            "fieldname": "machine",
            "fieldtype": "Link",
            "options": "Machine",
        },
        {
            "label": "Operation",
            "fieldname": "operation",
            "fieldtype": "Link",
            "options": "Operation Master",
            "width": 200,
        },
        // {
        //     "label": "Frequency",
        //     "fieldname": "frequency",
        //     "fieldtype": "Select",
        //     "options": ["Daily", "Monthly", "Quarterly"],
        //     "width": 200,
        //     "reqd": 1,
        // },
    ]
}
