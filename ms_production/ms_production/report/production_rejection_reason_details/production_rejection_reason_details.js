// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Production Rejection Reason Details"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			
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
			fieldname: "Rejection_Reason",
			fieldtype: "Link",
			label: "Rejection Reason",
			options: "Rejection Reason",
		},
		{
			fieldname: "Operator_Name",
			fieldtype: "Link",
			label: "Operator Name",
			options: "Operator Master",
			
		},
		{
			fieldname: "Supervisor_Name",
			fieldtype: "Link",
			label: "Supervisor Name",
			options: "Supervisor Master",
			
		},
		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
