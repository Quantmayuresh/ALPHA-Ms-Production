# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
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
			"fieldname" : "finished_item",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Finished Item",
			"width":150
		},
		{
			"fieldname" : "qty",
			"fieldtype" : "Float",
			"label" : "Quantity",
			"precision": 3,
			"width":120
		},
			
		# {
		# 	"fieldname" : "grade",
		# 	"fieldtype" : "Data",
		# 	"label" : "Grade"			
		# },
		{
			"fieldname" : "rejection_reason",
			"fieldtype" : "Data",
			"label" : "Rejection Reason"
		},
		{
			"fieldname" : "rejection_type",
			"fieldtype" : "Data",
			"label" : "Rejection Type"
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
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
						d.name 'name',
						d.company 'company',
						d.supervisor 'supervisor',
						d.supervisor_name 'supervisor_name',
						d.downstream_process 'downstream_process',
						r.finished_item 'finished_item',
						SUM(r.qty) 'qty',
						r.rejection_reason 'rejection_reason',
						r.rejection_type 'rejection_type'												
					FROM
						`tabDownstream Processes` d
					LEFT JOIN
						`tabDownstream Item Rejection Reason` r ON d.name = r.parent
					WHERE
						d.company = %s AND DATE(d.date) BETWEEN %s AND %s AND d.docstatus = 1					
				"""
	if sup_name:
		add_condition(conditions, params, "d.supervisor = %s", sup_name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY d.name, d.company, d.supervisor, d.supervisor_name, d.downstream_process, r.finished_item, r.rejection_reason, r.rejection_reason,  r.rejection_type"

	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data
 