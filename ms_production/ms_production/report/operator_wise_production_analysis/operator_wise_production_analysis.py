# Copyright (c) 2024, Abhishek Chougule and contributors
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
			'fieldname': "operator",
			'fieldtype': "Link",
			'label': "Operator Id",
			'options': "Operator Master",

		},
        {
			'fieldname': "operator_name",
			'fieldtype': "Data",
			'label': "Operator Name",

		},
        {
			'fieldname': "supervisor",
			'fieldtype': "Link",
			'label': "Supervisor Id",
			'options': "Supervisor Master",

		},
          {
			'fieldname': "supervisor_name",
			'fieldtype': "Data",
			'label': "Supervisor Name",

		},
          {
			'fieldname': "operation",
			'fieldtype': "Link",
			'label': "Operation",
			'options':"Operation Master",
		},
           {
			'fieldname': "operation_name",
			'fieldtype': "Data",
			'label': "Operation Name",
		},
             {
			'fieldname': "item",
			'fieldtype': "Link",
			'label': "Item",
			'options': "Item",
		},
		{
			'fieldname': "finished_item_name",
			'fieldtype': "Data",
			'label': "Finished Item Name",
		},
          {
			'fieldname': "ok_qty",
			'fieldtype': "Float",
			'label': "OK Qty",
		},
		 {
			'fieldname': "percentage_OK_Qty",
			'fieldtype': "Float",
			'label': "Percentage OK Qty",
		},
          {
			'fieldname': "cr_qty",
			'fieldtype': "Float",
			'label': "CR Qty",
		},
           {
			'fieldname': "Percentage_CR_Qty",
			'fieldtype': "Float",
			'label': "Percentage CR Qty",
		},
            {
			'fieldname': "mr_qty",
			'fieldtype': "Float",
			'label': "MR Qty",
		},
              {
			'fieldname': "Percentage_MR_Qty",
			'fieldtype': "Float",
			'label': "Percentage MR Qty",
		},
               {
			'fieldname': "rw_qty",
			'fieldtype': "Float",
			'label': "RW Qty",
		},
               {
			'fieldname': "Total_Qty",
			'fieldtype': "Float",
			'label': "Total Qty",
		},
                 {
			'fieldname': "Earned_Hours",
			'fieldtype': "Float",
			'label': "Earned Hours",
		},
                 {
			'fieldname': "Efficiency",
			'fieldtype': "Float",
			'label': "Efficiency",
		},
        {
			'fieldname': "Machine",
			'fieldtype': "Data",
			'label': "Machine",
			# 'options':"Machine",
		},
           {
			'fieldname': "Total_Rejection",
			'fieldtype': "Float",
			'label': "Total Rejection",
		},
	]


def get_data(filters):
	
	company = filters.get('company')
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	operator = filters.get('operator')
	supervisor =  filters.get('supervisor')
	item =  filters.get('item')
	operation =  filters.get('operation')
	conditions = []
	params = [from_date, to_date ,company]
     


	sql_query = """
			select
			CASE WHEN p.operator is null  THEN "Missing Operator" ELSE p.operator END AS operator,
			CASE WHEN p.operator_name is null  THEN "-" ELSE p.operator_name END AS operator_name,
			p.supervisor as supervisor,
			p.supervisor_name supervisor_name,
			q.operation operation,
			q.operation_name operation_name,
			q.item item,
			q.finished_item_name finished_item_name,
			sum(q.ok_qty) ok_qty,
			(sum(q.ok_qty) / sum(q.total_qty)) * 100  percentage_OK_Qty,
			sum(q.cr_qty) cr_qty,
			(sum(q.cr_qty) / sum(q.total_qty)) * 100  "Percentage_CR_Qty",
			sum(q.mr_qty)  mr_qty,
			(sum(q.mr_qty) / sum(q.total_qty)) * 100  Percentage_MR_Qty,
			sum(q.rw_qty) rw_qty,
			(sum(q.rw_qty) / sum(q.total_qty)) * 100  Percentage_RW_Qty,
			sum(q.total_qty) Total_Qty,
			sum(q.earned_min)/60 Earned_Hours,
			ROUND((sum(q.earned_min)/60) / (SUM(p.required_time)/60) *100,2) "Efficiency",
			q.machine "Machine",
			sum(q.cr_qty+q.mr_qty+q.rw_qty) as 'Total_Rejection'
		
		from 
			`tabProduction` p
		left join 
			`tabQty Details` q on p.name = q.parent
		where 
			p.date between  %s AND %s 
			and p.company = %s 
			and p.docstatus = 1
		
												
					"""
		
		
	if operator:
		conditions.append("p.operator = %s")
		params.append(operator)

	
	if supervisor:
		conditions.append("p.supervisor = %s")
		params.append(supervisor)
		
	if operation:
		conditions.append("q.operation = %s")
		params.append(operation)

	
	if item:
		conditions.append("q.item = %s")
		params.append(item)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """
			group by 
			p.operator, p.operator_name, q.operation,q.operation_name,q.item, q.finished_item_name,
			CASE  WHEN p.operator = "None" THEN "Missing Operator" ELSE p.operator END,
			CASE  WHEN p.operator_name = "None" THEN "-" ELSE p.operator_name END
				"""
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data