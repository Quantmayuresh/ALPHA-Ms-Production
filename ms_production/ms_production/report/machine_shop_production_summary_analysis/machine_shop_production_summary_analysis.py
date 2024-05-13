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
	company = filters.get("company")
	f_date = filters.get("f_date")
	t_date = filters.get("t_date")
	supervisor = filters.get("supervisor")
	operator = filters.get("operator")
	shift = filters.get("shift")
	finished_item = filters.get("finished_item")
	machine = filters.get("machine")
	operation = filters.get("operation")

	conditions = []
	params = [f_date,t_date,company]

	if f_date and t_date and company:
		# sql_query = """
		# 			SELECT qd.item, qd.finished_item_name, qd.ok_qty,qd.cr_qty,qd.mr_qty,qd.rw_qty,
   		# 				   qd.total_qty, qd.earned_min,qd.machine 'machine',p.supervisor,
        # 				   p.supervisor_name ,p.operator,p.operator_name,qd.operation,qd.operation_name
		# 			FROM `tabProduction` as p
		# 			LEFT JOIN `tabQty Details` as qd on p.name = qd.parent
		# 			WHERE 
		# 				p.date between  %s AND %s 
		# 				and p.company = %s 
		# 				and p.docstatus = 1
		# 			"""
		sql_query = """
				SELECT qd.item, qd.finished_item_name, sum(qd.ok_qty) "ok_qty", qd.operation,
					  sum(qd.ok_qty)/sum(qd.total_qty) as "ok_qty_per",
					  sum(qd.cr_qty)/sum(qd.total_qty) as "cr_qty_per",
					   sum(qd.mr_qty)/sum(qd.total_qty) as "mr_qty_per",
						sum(qd.rw_qty)/sum(qd.total_qty) as "rw_qty_per",
				      sum(qd.cr_qty) "cr_qty",sum(qd.mr_qty) "mr_qty", sum(qd.rw_qty) "rw_qty",
					  sum(qd.total_qty) "total_qty", qd.earned_min 'earned_min',qd.machine 'machine',p.supervisor 'supervisor',
				      p.supervisor_name 'supervisor_name',p.operator 'operator',p.operator_name 'operator_name',qd.operation 'operator',qd.operation_name 'operation_name'
				FROM `tabProduction` as p
				LEFT JOIN `tabQty Details` as qd on p.name = qd.parent
				where 
				p.date between  %s AND %s 
				and p.company = %s 
				and p.docstatus = 1
					"""
  
		if supervisor:
			conditions.append("p.supervisor = %s")
			params.append(supervisor)

		if operator:
			conditions.append("p.operator = %s")
			params.append(operator)

		if shift:
			conditions.append("p.shift_time = %s")
			params.append(shift)
   
		if finished_item:
			conditions.append("qd.item = %s")
			params.append(finished_item)

		if machine:
			conditions.append("qd.machine = %s")
			params.append(machine)

		if operation:
			conditions.append("qd.operation = %s")
			params.append(operation)
			
		if conditions:
			sql_query += " AND " + " AND ".join(conditions)
   
		sql_query += """
		Group by 
				qd.item, qd.finished_item_name,qd.machine
		"""

		data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
		return data

		

	