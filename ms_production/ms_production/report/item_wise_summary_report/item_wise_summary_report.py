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
			"label": _("Finished Item"),
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
			"label": _("Machine"),
        		"fieldname": "machine",
          		"fieldtype": "Data",
	           	"width": 100
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
	        },	{
			"label": _("Operator Name"),
	        	"fieldname": "operator_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },	{
			"label": _("Operation"),
	        	"fieldname": "operation",
	          	"fieldtype": "Data",
	           	"width": 150
	        },	{
			"label": _("Operation Name"),
	        	"fieldname": "operation_name",
	          	"fieldtype": "Data",
	           	"width": 150
	        },
			{
			"label": _("OK Qty"),
        		"fieldname": "ok_qty",
          		"fieldtype": "Int",
	           	"width": 100
	        },
   {
			"label": _("OK Qty in %"),
        		"fieldname": "ok_qty_per",
          		"fieldtype": "Float",
	           	"width": 100
	        },
  		{
			"label": _("CR Qty"),
	        	"fieldname": "cr_qty",
	          	"fieldtype": "Int",
	           	"width": 150
	        },
    {
			"label": _("CR Qty in %"),
	        	"fieldname": "cr_qty_per",
	          	"fieldtype": "Float",
	           	"width": 150
	        },
	{
			"label": _("MR Qty"),
        		"fieldname": "mr_qty",
          		"fieldtype": "int",
	           	"width": 100
	        },
 {
			"label": _("MR Qty in %"),
        		"fieldname": "mr_qty_per",
          		"fieldtype": "Float",
	           	"width": 100
	        },
  		{
			"label": _("RW Qty"),
	        	"fieldname": "rw_qty",
	          	"fieldtype": "Int",
	           	"width": 150
	        },
    {
			"label": _("RW Qty in %"),
	        	"fieldname": "rw_qty_per",
	          	"fieldtype": "Float",
	           	"width": 150
	        },
			{
			"label": _("Total Qty"),
        		"fieldname": "total_qty",
          		"fieldtype": "Int",
	           	"width": 100
	        },
  		{
			"label": _("Earned Min"),
	        	"fieldname": "earned_min",
	          	"fieldtype": "Int",
	           	"width": 150
	        },

	
	]

def get_data(filters):
    data = []
    flag=False
    query_filters = {"date": ['between', [filters.get('f_date'), filters.get('t_date')]], 
                                             "company": filters.get('company')}

    if filters.get("supervisor"):
        query_filters['supervisor']=filters.get("supervisor")
        
    if filters.get("shift"):
        query_filters['shift_time']=filters.get("shift")
    
    if filters.get("operator"):
        query_filters['operator']=filters.get("operator")  
    
        

    if filters.get('f_date') and filters.get('t_date') and filters.get('company'):
        docs = frappe.get_all("Production",query_filters )       
   
        for d in docs:
            production_doc = frappe.get_doc("Production", d['name'])
            qty_details = production_doc.get('qty_details')
            if qty_details:
                for qty_detail in qty_details:
                    for d in data:
                        if qty_detail.get("item")==d["item"] and qty_detail.get("finished_item_name")==d["finished_item_name"] and qty_detail.get("machine")==d["machine"]:
                            flag=True
                            d["ok_qty"] += qty_detail.get("ok_qty")
                            d["cr_qty"] += qty_detail.get("cr_qty")
                            d["mr_qty"] += qty_detail.get("mr_qty")
                            d["rw_qty"] += qty_detail.get("rw_qty")
                            d["total_qty"] += qty_detail.get("total_qty")
                            d["ok_qty_per"] =(d["ok_qty"]/d["total_qty"])*100
                            d["cr_qty_per"] = (d["cr_qty"]/d['total_qty'])*100
                            d["mr_qty_per"] = (d["mr_qty"]/d['total_qty'])*100
                            d["rw_qty_per"] = (d["rw_qty"]/d['total_qty'])*100
                    if not flag:
                        if filters.get("finished_item") == qty_detail.get("item") or filters.get("finished_item") == None:
                            if filters.get("machine") == qty_detail.get("machine") or filters.get("machine") == None:
                                if filters.get("operation") == qty_detail.get("operation") or filters.get("operation") == None:
                                    data.append({
											"item": qty_detail.get("item"),
											"finished_item_name": qty_detail.get("finished_item_name"),
											"ok_qty": qty_detail.get("ok_qty"),
											"ok_qty_per":(qty_detail.get("ok_qty")/qty_detail.get("total_qty"))*100,
											"cr_qty": qty_detail.get("cr_qty"),
											"cr_qty_per":(qty_detail.get("cr_qty")/qty_detail.get("total_qty"))*100,
											"mr_qty": qty_detail.get("mr_qty"),
											"mr_qty_per":(qty_detail.get("mr_qty")/qty_detail.get("total_qty"))*100,
											"rw_qty": qty_detail.get("rw_qty"),
											"rw_qty_per":(qty_detail.get("rw_qty")/qty_detail.get("total_qty"))*100,
											"total_qty": qty_detail.get("total_qty"),
											"earned_min": qty_detail.get("earned_min"),
											"machine": qty_detail.get("machine"),
											"supervisor": production_doc.supervisor,
											"supervisor_name": production_doc.supervisor_name,
											"operator": production_doc.operator,
											"operator_name": production_doc.operator_name,
											"operation": qty_detail.get("operation"),
											"operation_name": qty_detail.get("operation_name")
									})
                   
                            
                    flag=False
    else:
        frappe.throw("Company,From Date and To Date is Mandatory")
    return data



