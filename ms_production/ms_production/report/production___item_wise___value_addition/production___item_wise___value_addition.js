// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Production - Item Wise - Value Addition"] = {
	"filters": [
		{
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
            "reqd": 1,
        },
        {
            "label": "From Date",
            "fieldname": "f_date",
            "fieldtype": "Date",
            "width": 200,
            "reqd": 1,
        },
        {
            "label": "To Date", 
            "fieldname": "t_date", 
            "fieldtype": "Date",
            "reqd": 1,
            
        },
	]
};
