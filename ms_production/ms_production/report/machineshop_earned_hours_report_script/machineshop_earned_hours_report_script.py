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
		{
			"fieldname": "Operation_Name",
			"fieldtype": "Link",
			"label": "Operation Name",
			"options": "Production",
		},
		{
			"fieldname": "Supervisor_Name",
			"fieldtype": "Link",
			"label": "Supervisor Name",
			"options": "Production",
			
		},
		{
			"fieldname": "Shift_Time",
			"fieldtype": "Link",
			"label": "Shift Time",
			"options": "Production",
		},
				{
			"fieldname": "Finished_Item_Name",
			"fieldtype": "Link",
			"label": "Finished Item Name",
			"options": "Qty Details",
		},
		{
			"fieldname": "Machine",
			"fieldtype": "Data",
			"label": "Machine",
			# "options": "Qty Details",
		},
		{
			"fieldname": "Earned_Hours",
			"fieldtype": "Float",
			"label": "Earned Hours",
			# "options": "Customer",
		},
		{
			"fieldname": "Efficiency",
			"fieldtype": "Float",
			"label": "Efficiency",
		},
		{
			"fieldname": "OK_QTY",
			"fieldtype": "Float",
			"label": "OK QTY",
			# "options": "Item",
		},
		{
			"fieldname": "OK_Weight",
			"fieldtype": "Float",
			"label": "OK Weight",
		},
		{
			"fieldname": "CR_QTY",
			"fieldtype": "Data",
			"label": "CR QTY",
			# "options": "Item",
		},
		{
			"fieldname": "CR_Weight",
			"fieldtype": "Float",
			"label": "CR Weight",
		},
				{
			"fieldname": "MR_QTY",
			"fieldtype": "Data",
			"label": "MR QTY",
			# "options": "Item",
		},
		{
			"fieldname": "MR_Weight",
			"fieldtype": "Float",
			"label": "MR Weight",
		},
				{
			"fieldname": "RW_QTY",
			"fieldtype": "Data",
			"label": "RW QTY",
			# "options": "Item",
		},
		{
			"fieldname": "RW_Weight",
			"fieldtype": "Float",
			"label": "RW Weight",
		},
		{
			"fieldname": "Total_QTY",
			"fieldtype": "Float",
			"label": "Total QTY",
		},
		{
			"fieldname": "Total_Weight",
			"fieldtype": "Float",
			"label": "Total Weight",
		},
		{
			"fieldname": "Down_Time",
			"fieldtype": "Float",
			"label": "Down Time",
		},
		{
			"fieldname": "Operation_ID",
			"fieldtype": "Data",
			"label": "Operation ID",
		},
		{
			"fieldname": "Supervisor_ID",
			"fieldtype": "float",
			"label": "Supervisor ID",
		},
		{
			"fieldname": "Finished_Item",
			"fieldtype": "Data",
			"label": "Finished Item",
		},
		{
			"fieldname": "Company",
			"fieldtype": "Data",
			"label": "Company",
		},
	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	operator_name = filters.get('operator_name')
	supervisor_name =  filters.get('supervisor_name')
	machine =  filters.get('Machine')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
			select
				p.operator_name AS 'Operator_Name',
				q.operation_name AS 'Operation_Name',
				p.supervisor_name 'Supervisor_Name',
				p.shift_time AS 'Shift_Time',
				q.finished_item_name AS 'Finished_Item_Name',
				q.machine AS 'Machine',
				SUM(q.earned_min)/60 'Earned_Hours',
				(sum(q.earned_min)/60) / (SUM(p.required_time)/60) *100 "Efficiency",
				SUM(q.ok_qty) AS 'OK_QTY',
				(SUM(q.ok_qty) * pu.value_per_unit) AS 'OK_Weight',
				SUM(q.cr_qty) AS 'CR_QTY',
				(SUM(q.cr_qty) * pu.value_per_unit) AS 'CR_Weight',
				SUM(q.mr_qty) AS 'MR_QTY', 
				(SUM(q.mr_qty) * pu.value_per_unit) AS 'MR_Weight',
				SUM(q.rw_qty) AS 'RW_QTY', 
				(SUM(q.rw_qty) * pu.value_per_unit) AS 'RW_Weight',
				SUM(q.total_qty) AS 'Total_QTY',
				(SUM(q.total_qty) * pu.value_per_unit) AS 'Total_Weight',
				SUM((SELECT SUM(d.time) FROM `tabDowntime Reason Details` d WHERE d.parent = p.name)) AS 'Down_Time',
				p.operator AS 'Operator_ID',
				q.operation AS 'Operation_ID',
				p.supervisor 'Supervisor_ID',
				q.item AS 'Finished_Item',
				p.company AS 'Company'
			FROM
				`tabProduction` p
			LEFT JOIN
				`tabQty Details` q ON p.name = q.parent
			LEFT JOIN 
				`tabProduction UOM Definition` pu ON q.item = pu.parent AND pu.uom = 'Kg'
			WHERE
				p.docstatus = '1' 
				AND p.date BETWEEN %s AND %s
				AND p.company = %s
			"""


	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	if operator_name:
		conditions.append("p.operator_name = %s")
		params["operator_name"] = operator_name

	if supervisor_name:
		conditions.append("p.supervisor_name = %s")
		params.append(supervisor_name)

	if machine:
		conditions.append("q.machine = %s")
		params.append(machine)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """GROUP BY q.item, q.machine, p.operator, p.operator_name """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data