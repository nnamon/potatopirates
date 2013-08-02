from velocity.models import *
import operator
from django.core.exceptions import ObjectDoesNotExist

def get_receipts_containing_item(item, excl=None):
    # item is a product id
    # excl should be a Purchase instance
    results = Purchase.objects.filter(product_id=item)
    receipts = set()
    for i in results:
        if not i == excl:
            receipts.add(i.receipt_id)
    return receipts

def others_also_bought(product):
    # product is a Product instance
    receipts = get_receipts_containing_item(product)
    product_histogram = {}
    for i in receipts:
        purchases = Purchase.objects.filter(receipt_id=i)
        for j in purchases:
            if j.product_id == product:
                break
            if product_histogram.has_key(j.product_id):
                product_histogram[j.product_id] += 1
            else:
                product_histogram[j.product_id] = 1
    sorted_phist = sorted(product_histogram.iteritems(), key=operator.itemgetter(1))
    sorted_phist.reverse()
    return sorted_phist[:5]

def popular_products():
    product_histogram = {}
    for i in Purchase.objects.all():
        if product_histogram.has_key(i.product_id):
            product_histogram[i.product_id] += 1
        else:
            product_histogram[i.product_id] = 1
    sorted_phist = sorted(product_histogram.iteritems(), key=operator.itemgetter(1))
    sorted_phist.reverse()
    return sorted_phist

def customer_trends(crfid):
    try:
        customer = CustomerProfile.objects.filter(rfid=crfid)
        receipts = Receipt.objects.filter(customer_id=customer)
        product_histogram = {}
        for i in receipts:
            purchases = Purchase.objects.filter(receipt_id=i)
            for j in purchases:
                if product_histogram.has_key(j.product_id):
                    product_histogram[j.product_id] += 1
                else:
                    product_histogram[j.product_id] = 1
        sorted_phist = sorted(product_histogram.iteritems(), key=operator.itemgetter(1))
        sorted_phist.reverse()
        return sorted_phist
    except ObjectDoesNotExist:
        return None

def customer_trends_also_bought(crfid):
    ctrends = customer_trends(crfid)[:5]
    personal_rec = []
    for i in ctrends:
        rec = others_also_bought(i[0])[0]
        personal_rec.append((rec[0], i[0]))
    return personal_rec
    
        
def main():
    p = Purchase.objects.all()[10]
    a = get_receipts_containing_item(p.product_id, p)
    for i in a:
        print Purchase.objects.filter(receipt_id=i)

if __name__=="__main__":
    main()
