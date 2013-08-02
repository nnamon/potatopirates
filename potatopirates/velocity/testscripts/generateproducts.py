import requests
import datetime
import random
import json

store = 1

def generate_random_item():
    prefixes = ['Shoddy', 'Amazing', 'Awesome', 'Poor', 'Evil', 'Good', 'Smelly', 'Rosy', 'Intelligent' , 'Round', 'Squarish', 'Boring', 'Exciting', 'Pretty', 'Ugly', 'Long', 'Short', 'Corny', 'Murderous']
    subject = ['Ant', 'Shoe', 'Balloon', 'Bottle', 'Stick', 'Mouse', 'Dog', 'Paper', 'Case', 'Laptop', 'Wall', 'Boot', 'Shorts', 'Cap', 'Hat', 'Reindeer', 'Pen', 'Box']
    p1 = random.choice(prefixes)
    p2 = random.choice(prefixes)
    s = random.choice(subject)
    pricelow = random.randrange(1, 99)/100.0
    pricehigh = random.randrange(1, 9999)
    price = pricelow + pricehigh
    return ["%s %s %s" % (p1, p2, s), price, store]

no = 20
json_p = []
for i in range(no):
    product = generate_random_item() 
    fields = {"name": product[0], "price": product[1], "store_id": product[2]}
    curr = {"pk": i, "model": "velocity.product", "fields": fields}
    json_p.append(curr)

print json.dumps(json_p)
