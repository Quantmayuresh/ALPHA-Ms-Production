// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Downstream Process Analysis"] = {
	"filters": [
		{
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company",
			"reqd" : 1
        }, 
        {
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
			"reqd" : 1
        },   
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
			"reqd" : 1
        },
		// {
        //     "fieldname": "item",
        //     "fieldtype" : "Link",
		// 	"options" : "item",
        //     "label": "Finished item"
	    // },
		{
            "fieldname": "downstream_process",
            "fieldtype" : "Link",
			"options" : "Downstream Processes Master",
            "label": "Downstream Processes"
	    },
        {
            "fieldname": "supervisor",
            "fieldtype" : "Link",
			"options" : "Supervisor Master",
            "label": "Supervisor"
	    }
	]
};
