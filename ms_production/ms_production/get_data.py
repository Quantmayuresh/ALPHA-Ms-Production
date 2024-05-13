import frappe
from frappe.model.document import Document


@frappe.whitelist()
def get_docs(f_date, t_date, company, customer):
    job_dict = {}
    
    # frappe.throw(str(company)+"============= "+str(customer))
    jobwr = frappe.get_all("Job Work Receipt", 
                           filters={'posting_date': ["between", [f_date, t_date]], 
                                    'company': company, 
                                     'customer_name': customer, 
                                    'is_return': True},
                           fields=["name"])
    # frappe.throw(str(jobwr))
    if jobwr:  
        job_dict['return_items'] = []
        for d in jobwr:
            doc1 = frappe.get_doc("Job Work Receipt", d.name)
            for i in doc1.get("return_items",{'is_fetched':False,'return_quantity':('>',0)}):
                doc_name = frappe.db.get_value("Delivery Note", {"custom_job_work_receipt": doc1.name}, "name")
                # frappe.throw(str(doc_name))
                item_data = {
                    "item_doc_name":d.name,
                    "item_code": i.item_code,
                    "item_name": i.item_name,
                    "challan_reference": i.challan_reference,
                    "returnable_quantity": i.returnable_quantity,
                    "as_it_is": i.as_it_is,
                    "cr_rejection": i.cr_rejection,
                    "mr_rejection": i.mr_rejection,
                    "other_rejection": i.other_rejection,
                    "return_quantity": i.return_quantity,
                    "total_quantity": i.total_quantity,
                    "source_warehouse": i.source_warehouse,
                    "available_quantity": i.available_quantity,
                    "reference_id": i.reference_id,
                    "delivery_note":doc_name,
                    "name1":i.name
                }
                job_dict['return_items'].append(item_data)
    else:
        frappe.throw("No Data Found")
        return
    # frappe.throw(str(job_dict))

    unique_items = {}

    for item in job_dict['return_items']:
        name = item['item_code']
        if name not in unique_items:
            jwr = frappe.get_doc("Job Work Receipt",item['challan_reference'])
            sales_order = frappe.get_doc("Sales Order",jwr.order_no)
            for d in sales_order.get("items"):
                if d.item_code == item['item_code']:
                    item['rate']=d.rate
                    break
            # frappe.throw(str(item['rate'])+"          "+ str(item))
            unique_items[name] = item.copy()

        else:
            dup_total = item['total_quantity']
            uniq_item = unique_items[name]
            uniq_total = uniq_item['total_quantity']
            total = dup_total + uniq_total
            unique_items[name]['total_quantity'] = total

            dup_ret_total = item['return_quantity']
            uniq_ret_item = unique_items[name]
            uniq_total = uniq_item['return_quantity']
            total = dup_total + uniq_total
            unique_items[name]['return_quantity'] = total

            dup_returnable_total = item['returnable_quantity']
            uniq_returnable_item = unique_items[name]
            uniq_returnable_total = uniq_returnable_item['returnable_quantity']
            total = dup_returnable_total + uniq_returnable_total
            unique_items[name]['returnable_quantity'] = total
            
    unique_items_list = list(unique_items.values())

    subcnt_doc = frappe.get_doc("Subcontracting Setting",{'name':company})
    description = frappe.get_value("Item",{'name':subcnt_doc.labour_invoice_item__code},'description')
    item_doc = frappe.get_doc("Item",{'name':subcnt_doc.labour_invoice_item__code})
    inc_acc = item_doc.get("item_defaults")[0].income_account

    # frappe.throw(str(inc_acc))
    
    return [job_dict,unique_items_list,subcnt_doc,description,inc_acc]


    
