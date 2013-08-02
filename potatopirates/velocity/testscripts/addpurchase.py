import requests
import datetime
import random
import json

rid = "90D9B"
timenow = datetime.datetime.now().isoformat()

purchases = []
for i in range(random.randrange(0, 10)):
    purchases.append(random.randrange(0,100))

data = {'time': timenow, 'purchases': json.dumps(purchases)}
a=requests.post("http://127.0.0.1:8000/%s/purchased/" % rid, data=data)
print a.text

