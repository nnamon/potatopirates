from django.shortcuts import render
from django.http import HttpResponse
from velocity.models import CustomerProfile, Receipt, Purchase, Product
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.decorators.csrf import csrf_exempt
import dateutil.parser
from velocity.analytics import *

def getCustomerProfile(rid):
    try:
        customer_l = CustomerProfile.objects.get(rfid=rid)
        return customer_l
    except ObjectDoesNotExist:
        return False
    
# Create your views here.

def login(request, rid):
    if getCustomerProfile(rid):
        return HttpResponse("1")
    else:
        return HttpResponse("0")

def purchases(request, rid):
    customer = getCustomerProfile(rid)
    if customer:
        receipts = Receipt.objects.filter(customer_id=customer.id)
        data = {}
        for i in receipts:
            key = i.time.isoformat() 
            data[key] = []
            purchases = Purchase.objects.filter(receipt_id=i)
            for j in purchases:
                product = j.product_id
                curr_p = {'pid': product.id, 'name': product.name, 'price': float(j.price), 'store': product.store_id.name}
                data[key].append(curr_p)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("0")

@csrf_exempt
def purchased(request, rid):
    customer = getCustomerProfile(rid)
    if customer and request.method == "POST":
        time = request.POST.get('time', '')
        purchases = json.loads(request.POST.get('purchases', ''))
        r = Receipt(customer_id=customer, time=dateutil.parser.parse(time))
        r.save()
        for i in purchases:
            pr = Product.objects.get(id=i)
            p = Purchase(receipt_id=r, product_id=pr, price=pr.price)
            p.save()
        return HttpResponse("1")
    else:
        return HttpResponse("0")

def recommended(request, rid):
    customer = getCustomerProfile(rid)
    if customer:
        suggest_pair = customer_trends_also_bought(rid)
        products = []
        for i in suggest_pair:
            rec = i[0]
            bec = i[1]
            r_p = {'pid': rec.id, 'name': rec.name, 'price': float(rec.price), 'store': rec.store_id.name}
            b_p = {'pid': bec.id, 'name': bec.name, 'price': float(bec.price), 'store': bec.store_id.name}
            fields = {'recommendation': r_p, 'because': b_p}
            products.append(fields)
        return HttpResponse(json.dumps(products))
    else:
        return HttpResponse("0")

def popular(request):
    products = []
    for i in popular_products()[:10]:
        p = i[0]
        curr_p = {'pid': p.id, 'name': p.name, 'price': float(p.price), 'store': p.store_id.name}
        products.append(curr_p)
    return HttpResponse(json.dumps(products))

def productothersbought(request, pid):
    try:
        product = Product.objects.get(id=pid)
        othersbought = others_also_bought(product)
        products = []
        for i in othersbought:
            p = i[0]
            curr_p = {'pid': p.id, 'name': p.name, 'price': float(p.price), 'store': p.store_id.name}
            products.append(curr_p)
        return HttpResponse(json.dumps(products))
    except ObjectDoesNotExist:
        return HttpResponse("0")

def statistics(request, rid):
    customer = getCustomerProfile(rid)
    if customer:
        receipts = Receipt.objects.filter(customer_id=customer)
        total_spent = 0
        no_purchases = 0
        for i in receipts:
            purchases = Purchase.objects.filter(receipt_id=i)
            for i in purchases:
                total_spent += i.price
                no_purchases += 1
        stats = {'total_spent': float(total_spent), 'times_shopped': len(receipts), 'items_purchased': no_purchases}
        return HttpResponse(json.dumps(stats))
    else:
        return HttpResponse("0")
