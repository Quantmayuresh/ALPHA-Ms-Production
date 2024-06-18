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
			"fieldname": "Finished_Item",
			"fieldtype": "Data",
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
			"fieldname": "Rejection_Reason",
			"fieldtype": "Link",
			"label": "Rejection Reason",
			"options": "Rejection Reason",
			
		},
		{
			"fieldname": "Rejection_Type",
			"fieldtype": "Data",
			"label": "Rejection Type",
			# "options": "Supervisor Master",
		},
		{
			"fieldname": "Qty",
			"fieldtype": "Float",
			"label": "Qty",
			# "options": "Supervisor Master",
		},
		{
			"fieldname": "Weight",
			"fieldtype": "Float",
			"label": "Weight",
			# "options": "Supervisor Master",
		},
		{
			"fieldname": "Company",
			"fieldtype": "Data",
			"label": "Company",
			# "options": "Pouring",
		},
		# {
		# 	"fieldname": "Burning_Loss_Weight",
		# 	"fieldtype": "Data",
		# 	"label": "Burning Loss Weight",
		# 	# "options": "Pouring",			
		# },
		# {
		# 	"fieldname": "Total_pouring_weight",
		# 	"fieldtype": "Float",
		# 	"label": "Total pouring weight",
		# 	# "options": "Pouring",
			
		# },
		# {
		# 	"fieldname": "Percentage_Burning_Loss",
		# 	"fieldtype": "Float",
		# 	"label": "Percentage Burning Loss",
		# 	# "options": "Pouring",
			
		# },								




	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	# Furnace = filters.get('furnece')
	Rejection_Reason = filters.get('Rejection_Reason')
	# Supervisor_Name =  filters.get('Supervisor_ID')
	company =  filters.get('Company')
	conditions = []
	params = [company, from_date, to_date]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(sql_query))


	sql_query = """
				SELECT 
					#p.name 'ID',
					#sp.date 'Date',
					i.finished_item 'Finished_Item',
					i.finished_item_name 'Finished_Item_Name',
					i.rejection_reason 'Rejection_Reason',
					i.rejection_type 'Rejection_Type',
					SUM(i.qty) 'Qty',
					(SUM(i.qty) * pi.value_per_unit) 'Weight',
					p.company 'Company'
				FROM
					`tabItem Rejection Reason` i
				LEFT JOIN
					`tabProduction` p ON p.name = i.parent
				LEFT JOIN
				    `tabProduction UOM Definition` pi ON i.finished_item = pi.parent
				WHERE
					p.company = %s
					AND p.date BETWEEN %s AND %s
					AND p.docstatus = 1
												
				"""


	if Rejection_Reason:
		conditions.append("i.rejection_reason IN ({0})".format(', '.join(['%s']*len(Rejection_Reason))))
		params.extend(Rejection_Reason)



	# if Supervisor_Name:
	# 	conditions.append("supervisor = %s")
	# 	params.append(Supervisor_Name)

	# if Casting_Treatment:
	# 	conditions.append("c.casting_treatment = %s")
	# 	params.append(Casting_Treatment)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY
					i.finished_item,
					i.finished_item_name,
					i.rejection_reason,
					i.rejection_type
				 """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data