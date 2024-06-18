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
			"fieldname": "Item_Code",
			"fieldtype": "Link",
			"label": "Item Code",
			"options": "Item",
		},
		{
			"fieldname": "Finished_Item",
			"fieldtype": "Link",
			"label": "Item Name",
			"options": "Item",
		},
		# {
		# 	"fieldname": "Finished_Item_Name",
		# 	"fieldtype": "Link",
		# 	"label": "Finished Item Name",
		# 	"options": "Item",
		# },
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
			"fieldtype": "Link",
			"label": "Company",
			"options": "company",
		},
		
	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	Rejection_Type = filters.get('Rejection_Type')
	company =  filters.get('Company')
	conditions = []
	params = [company, from_date, to_date]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(sql_query))


	sql_query = """
                SELECT 
					i.finished_item 'Item_Code',
					itm.item_name 'Finished_Item',
					i.rejection_reason 'Rejection_Reason',
					i.rejection_type 'Rejection_Type',
					SUM(i.qty) 'Qty',
					SUM(i.qty) * w.value_per_unit 'Weight',
					d.company 'Company'
				FROM
					`tabDownstream Item Rejection Reason` i
				LEFT JOIN
					`tabDownstream Processes` d ON d.name = i.parent
				LEFT JOIN
					`tabProduction UOM Definition` w ON w.parent = i.finished_item
				LEFT JOIN
					`tabItem` itm ON itm.name = i.finished_item
				WHERE
					d.docstatus = 1
					AND d.company = %s
					AND d.date BETWEEN %s AND %s
												
				"""


	# if Rejection_Reason:
	# 	conditions.append("i.rejection_reason IN ({0})".format(', '.join(['%s']*len(Rejection_Reason))))
	# 	params.extend(Rejection_Reason)



	if Rejection_Type:
		conditions.append("i.rejection_type = %s")
		params.append(Rejection_Type)

	# if Casting_Treatment:
	# 	conditions.append("c.casting_treatment = %s")
	# 	params.append(Casting_Treatment)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY
                    i.finished_item,
                    i.rejection_reason,
                    i.rejection_type
				 """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data