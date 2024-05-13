# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
    return [
  		{
			"label": _("Finished Item Code"),
        		"fieldname": "item",
          		"fieldtype": "Data",
	           	"width": 100
	        },
  		{
			"label": _("Finished Item Name"),
	        	"fieldname": "finished_item_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
    
         	{
			"label": _("OK Quantity"),
        		"fieldname": "ok_qty",
          		"fieldtype": "Int",
	           	"width": 100
	        },
         {
			"label": _("Machine"),
        		"fieldname": "machine",
          		"fieldtype": "Data",
	           	"width": 100
	        },
         {
			"label": _("Operation"),
	        	"fieldname": "operation",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
         		{
			"label": _("Operation Name"),
	        	"fieldname": "operation_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
         {
			"label": _("Operator Name"),
	        	"fieldname": "operator_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
   			 {
			"label": _("Supervisor Id"),
	        	"fieldname": "supervisor",
	          	"fieldtype": "Data",
	           	"width": 150
	        },	{
			"label": _("Supervisor Name"),
	        	"fieldname": "supervisor_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },	{
			"label": _("Operator Id"),
	        	"fieldname": "operator",
	          	"fieldtype": "Data",
	           	"width": 150
	        },	
         {
			"label": _("Amount"),
        		"fieldname": "amt",
          		"fieldtype": "Int",
	           	"width": 100
	        },
		
  		{
			"label": _("Operator Id"),
	        	"fieldname": "operator",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
    {
			"label": _("Operator Name"),
	        	"fieldname": "operator_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
	{
			"label": _("Supervisor Id"),
        		"fieldname": "supervisor",
          		"fieldtype": "Data",
	           	"width": 100
	        },
 {
			"label": _("Supervisor Name"),
        		"fieldname": "supervisor_name",
          		"fieldtype": "Data",
	           	"width": 100
	        },
  		{
			"label": _("Company"),
	        	"fieldname": "company",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
    
	
	]
    
def get_data(filters):
    company = filters.get("company")
    f_date = filters.get("f_date")
    t_date = filters.get("t_date")
    params = [f_date,t_date,company]
    
    sql_query = """  select q.item, q.finished_item_name , q.ok_qty,  q.machine, q.operation, q.operation_name, mt.operation_rate *q.ok_qty as 'amt', 
						p.operator, p.operator_name, p.supervisor, p.supervisor_name, p.company
						FROM `tabQty Details` q
						inner join (select q.item, q.name, m.operation_rate, m.operation
									FROM `tabMaterial Cycle Time` q
									inner join  `tabMachine Item` m on m.parent = q.name
									) mt
									on mt.item = q.item and q.operation = mt.operation 
						inner join `tabProduction` p on p.name = q.parent
						where  p.docstatus = '1' 
						AND p.date BETWEEN %s AND %s
						AND p.company = %s
                         
                         """
                         
    data = frappe.db.sql(sql_query,tuple(params),as_dict=1)
    
    return data