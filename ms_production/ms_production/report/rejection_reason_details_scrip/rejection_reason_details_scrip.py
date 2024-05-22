# Copyright (c) 2024, quantdairy and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data


def get_columns(filters):
	return [
		{
			"fieldname": "Operator_Name",
			"fieldtype": "Link",
			"label": "Operator Name",
			"options": "Production",
		},
		# {
		# 	"fieldname": "Operation_Name",
		# 	"fieldtype": "Link",
		# 	"label": "Operation Name",
		# 	"options": "Production",
		# },
		{
			"fieldname": "Supervisor_Name",
			"fieldtype": "Link",
			"label": "Supervisor Name",
			"options": "Production",
		},
		{
			"fieldname": "Rejection_Reason",
			"fieldtype": "Link",
			"label": "Rejection Reason",
			"options": "Item Rejection Reason",
		},
		{
			"fieldname": "Finished_Item",
			"fieldtype": "Link",
			"label": "Finished Item",
			"options": "Item",
		},
		{
			"fieldname": "Finished_Item_Name",
			"fieldtype": "Link",
			"label": "Finished Item Name",
			"options": "Item",
		},
		{
			"fieldname": "QTY",
			"fieldtype": "Float",
			"label": "QTY",
			# "options": "Item Rejection Reason",
		},
		{
			"fieldname": "Total_Qty",
			"fieldtype": "Float",
			"label": "Total Qty",
		},
		{
			"fieldname": "Rejection_Percentage",
			"fieldtype": "Float",
			"label": "Rejection Percentage",
			# "options": "Item",
		},
		# {
		# 	"fieldname": "OK_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "OK Weight",
		# },
		# {
		# 	"fieldname": "CR_QTY",
		# 	"fieldtype": "Float",
		# 	"label": "CR QTY",
		# 	# "options": "Item",
		# },
		# {
		# 	"fieldname": "CR_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "CR Weight",
		# },
		# 		{
		# 	"fieldname": "MR_QTY",
		# 	"fieldtype": "Float",
		# 	"label": "MR QTY",
		# 	# "options": "Item",
		# },
		# {
		# 	"fieldname": "MR_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "MR Weight",
		# },
		# 		{
		# 	"fieldname": "RW_QTY",
		# 	"fieldtype": "Float",
		# 	"label": "RW QTY",
		# 	# "options": "Item",
		# },
		# {
		# 	"fieldname": "RW_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "RW Weight",
		# },
		# {
		# 	"fieldname": "Total_QTY",
		# 	"fieldtype": "float",
		# 	"label": "Total QTY",
		# },
		# {
		# 	"fieldname": "Total_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "Total Weight",
		# },
		# {
		# 	"fieldname": "Down_Time",
		# 	"fieldtype": "Float",
		# 	"label": "Down Time",
		# },
		# {
		# 	"fieldname": "Operation_ID",
		# 	"fieldtype": "float",
		# 	"label": "Operation ID",
		# },
		# {
		# 	"fieldname": "Supervisor_ID",
		# 	"fieldtype": "float",
		# 	"label": "Supervisor ID",
		# },
		# {
		# 	"fieldname": "Finished_Item",
		# 	"fieldtype": "float",
		# 	"label": "Finished Item",
		# },
		# {
		# 	"fieldname": "Company",
		# 	"fieldtype": "float",
		# 	"label": "Company",
		# },
	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	operator_name = filters.get('operator_name')
	Supervisor_Name =  filters.get('Supervisor_Name')
	rejection_reason =  filters.get('rejection_reason')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))

	sql_query = """
				SELECT 
					p.operator_name AS 'Operator_Name',
					p.supervisor_name AS 'Supervisor_Name',
					rr.rejection_reason AS 'Rejection_Reason',
					rr.finished_item AS 'Finished_Item',
					rr.finished_item_name AS 'Finished_Item_Name',
					SUM(rr.qty) AS 'QTY',
					SUM(total_qty) 'Total_Qty',
					ROUND((SUM(rr.qty) / SUM(total_qty)) *100,2) AS 'Rejection_Percentage'
				FROM
					`tabProduction` p
				LEFT JOIN
					`tabItem Rejection Reason` rr ON p.name = rr.parent
				WHERE 
					p.docstatus = '1'  
					AND p.date BETWEEN %s AND %s
					AND p.company = %s
					AND rr.rejection_reason is NOT NULL
				# ORDER BY
				# SUM(rr.qty);
			"""


	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	if operator_name:
		conditions.append("p.operator_name = %s")
		params["operator_name"] = operator_name

	if Supervisor_Name:
		conditions.append("p.supervisor_name = %s")
		params.append(Supervisor_Name)

	if rejection_reason:
		conditions.append("rr.rejection_reason = %s")
		params.append(rejection_reason)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY rr.rejection_reason, rr.finished_item """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data