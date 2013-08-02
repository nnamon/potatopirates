from django.shortcuts import render
from django.http import HttpResponse
from velocity.models import CustomerProfile, Receipt, Purchase, Product
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.decorators.csrf import csrf_exempt
import dateutil.parser

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
                curr_p = {'name': product.name, 'price': float(j.price), 'store': product.store_id.name}
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
    if getCustomerProfile(rid):
        return HttpResponse("recommended")
    else:
        return HttpResponse("0")
