// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Operator Wise Production Analysis"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			fieldtype: "Date",
			label: "From Date",
			default:'Today',
			reqd: 1,
		},
		{
			fieldname: "to_date",
			fieldtype: "Date",
			label: "To Date",
			default:'Today',
			reqd: 1,
		},
		{
			fieldname: "operator",
			fieldtype: "Link",
			label: "Operator",
			options: "Operator Master",
		},
		{
			fieldname: "supervisor",
			fieldtype: "Link",
			label: "Supervisor",
			options:"Supervisor Master",
		},
		{
			fieldname: "operation",
			fieldtype: "Link",
			label: "Operation",
			options:"Operation Master",
		},
		{
			fieldname: "item",
			fieldtype: "Link",
			label: "Finished Item",
			options:"Item",
		},
		 
	]
};
