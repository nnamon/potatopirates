import requests
import datetime
import random
import json

def generate_customer():
    hexc = ['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    cred = ""
    for i in range(5):
        cred += random.choice(hexc)
    return {'rfid': cred}

def generate_store():
    prefixes = ['Shoddy', 'Amazing', 'Awesome', 'Poor', 'Evil', 'Good', 'Smelly', 'Rosy', 'Intelligent' , 'Round', 'Squarish', 'Boring', 'Exciting', 'Pretty', 'Ugly', 'Long', 'Short', 'Corny', 'Murderous']
    unique = ['Hungarian', 'French', 'Japanese', 'European', 'Italian', 'Korean', '', 'Turkish', 'Mongolian', 'Hyperion']
    subject = ['Mansion', 'Boutique', 'Corner', 'Haven', 'Home', 'Diner', 'Shop', 'Store', 'Wares', 'Armoury', 'Restaurant', 'Eatery', 'Cosmetics']
    p1 = random.choice(prefixes)
    p2 = random.choice(unique)
    s = random.choice(subject)
    return {'name': "%s %s %s" % (p1, p2, s)}

def generate_random_item(no_of_stores):
    prefixes = ['Shoddy', 'Amazing', 'Awesome', 'Poor', 'Evil', 'Good', 'Smelly', 'Rosy', 'Intelligent' , 'Round', 'Squarish', 'Boring', 'Exciting', 'Pretty', 'Ugly', 'Long', 'Short', 'Corny', 'Murderous']
    subject = ['Ant', 'Shoe', 'Balloon', 'Bottle', 'Stick', 'Mouse', 'Dog', 'Paper', 'Case', 'Laptop', 'Wall', 'Boot', 'Shorts', 'Cap', 'Hat', 'Reindeer', 'Pen', 'Box']
    p1 = random.choice(prefixes)
    p2 = random.choice(prefixes)
    s = random.choice(subject)
    pricelow = random.randrange(1, 99)/100.0
    pricehigh = random.randrange(1, 9999)
    price = pricelow + pricehigh
    return {'name': "%s %s %s" % (p1, p2, s), 'price': price, 'store_id': random.randrange(1, no_of_stores)}

def j_entries(model, e):
    jp = []
    for i in range(len(e)):
        curr = {"pk": i, "model": model, "fields": e[i]}
        jp.append(curr)
    return jp

customers = []
for i in range(20):
    customers.append(generate_customer())

stores = []
for i in range(10):
    stores.append(generate_store())

products = []
for i in range(100):
    products.append(generate_random_item(len(stores)))

json_p = []
json_p += j_entries("velocity.customerprofile", customers)
json_p += j_entries("velocity.store", stores)
json_p += j_entries("velocity.product", products)

print json.dumps(json_p)

