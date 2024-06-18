# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data 
 
def get_columns():
	return[
		{
			"fieldname" : "name",
			"fieldtype" : "Link",
			"options": "Downstream Processes",
			"label" : "Document Id"
		},
		{
			"fieldname" : "date",
			"fieldtype" : "Date",
			"label" : "Date"
		},
		{
			"fieldname" : "supervisor",
			"fieldtype" : "Data",
			"label" : "Supervisor Id"
		},
		{
			"fieldname" : "supervisor_name",
			"fieldtype" : "Data",
			"label" : "Supervisor Name",
			"width":200
		},
		{
			"fieldname" : "downstream_process",
			"fieldtype" : "Data",
			"label" : "Downstream Processes",
			"width":180
		},	
		{
			"fieldname" : "item",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Finished Item Code",
			"width":150
		},
		{
			"fieldname" : "item_name",
			"fieldtype" : "Data",
			"label" : "Finished Item Name",
			"width":200
		},
		{
			"fieldname" : "Source_Warehouse",
			"fieldtype" : "Link",
			"options": "Warehouse",
			"label" : "Source Warehouse"
		},
		{
			"fieldname" : "Target_Warehouse",
			"fieldtype" : "Link",
			"options": "Warehouse",
			"label" : "Target_Warehouse"
		},
		{
			"fieldname" : "ok_qty",
			"fieldtype" : "Float",
			"label" : "OK Quantity",
			"precision": 3,
			"width":120
		},
		{
			"fieldname" : "cr_qty",
			"fieldtype" : "Float",
			"label" : "CR Quantity",
			"precision": 3,
			"width":120
		},
		{
			"fieldname" : "mr_qty",
			"fieldtype" : "Float",
			"label" : "MR Quantity",
			"precision": 3,
			"width":120
		},
		{
			"fieldname" : "rw_qty",
			"fieldtype" : "Float",
			"label" : "RW Quantity",
			"precision": 3,
			"width":120
		},
		{
			"fieldname" : "total_qty",
			"fieldtype" : "Float",
			"label" : "Total Quantity",
			"precision": 3,
			"width":120
		},
		{
			"fieldname" : "company",
			"fieldtype" : "Data",
			"label" : "Company"
		},	
	] 

 
def add_condition(condition_list, params_list, condition, param_value):
    if param_value:
        condition_list.append(condition)
        params_list.append(param_value) 
        
def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	comp = filters.get("company")
	sup_name = filters.get("supervisor") 
	item_code_name = filters.get("item") 
	downstream_process = filters.get("downstream_process")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
						dp.name 'name',
						dp.date 'date',
						dp.company 'company',
						dp.supervisor 'supervisor',
						dp.supervisor_name 'supervisor_name',
						dp.downstream_process 'downstream_process',
						dq.item 'item',
						d.item_name 'item_name',
						r.source_warehouse 'Source_Warehouse',
						d.target_warehouse 'Target_Warehouse',
						SUM(dq.ok_qty) 'ok_qty',
						SUM(dq.cr_qty) 'cr_qty',
						SUM(dq.mr_qty) 'mr_qty',
						SUM(dq.rw_qty) 'rw_qty',
						SUM(dq.total_qty) 'total_qty'											
					FROM 
						`tabDownstream Processes` dp
					LEFT JOIN
						`tabDownstream Qty Details` dq ON dp.name = dq.parent
					LEFT JOIN
						`tabDownstream Items Production` d ON dq.item = d.item and dp.name = d.parent
					LEFT JOIN
					    `tabDownstream Raw Items Production` r ON dq.item = r.item and dp.name = r.parent
					WHERE
						dp.company = %s AND DATE(dp.date) BETWEEN %s AND %s AND dp.docstatus = 1					

				"""
	if sup_name:
		add_condition(conditions, params, "dp.supervisor = %s", sup_name)

	if downstream_process:
		add_condition(conditions, params, "dp.downstream_process = %s", downstream_process)

	# if item_code_name:
	# 	add_condition(conditions, params, "dp.item = %s", item_code_name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY dp.name, dp.date, dp.company, dp.supervisor, dp.supervisor_name, dp.downstream_process, dq.item, d.item_name,r.source_warehouse, d.target_warehouse"

	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data
 