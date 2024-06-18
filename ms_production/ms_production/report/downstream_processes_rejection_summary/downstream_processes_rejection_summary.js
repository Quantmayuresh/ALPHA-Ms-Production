// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Downstream Processes Rejection Summary"] = {
	"filters": [
		{
			fieldname: "Company",
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
			fieldname: "Rejection_Type",
			fieldtype: "Link",
			label: "Rejection Type",
			options: "Rejection Type",
			
		},
		// {
		// 	fieldname: "Rejection_Reason",
		// 	label: __("Rejection Reason"),
		// 	fieldtype: "MultiSelectList",
		// 	options: "Rejection Reason",
		// 	get_data: function (txt) {
		// 		return frappe.db.get_link_options("Rejection Reason", txt, {
		// 			company: frappe.query_report.get_filter_value("Company"),
		// 		});
		// 	},
		// },
		// {
		// 	fieldname: "Operator_ID",
		// 	fieldtype: "Link",
		// 	label: "Operator Name",
		// 	options: "Operator Master",
		// },

		// {
		// 	fieldname: "Supervisor_ID",
		// 	fieldtype: "Link",
		// 	label: "Supervisor Name",
		// 	options: "Supervisor Master",
		// },
	]
};
