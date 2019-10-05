#ADITYA RANDIVE
#aditya.randive@nutanix.com

import time
import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

IP = '10.63.30.111'
USER = 'admin'
PASSWORD = 'nx2Tech290!'

# (1) Make Session
session = requests.Session()
session.auth = (USER, PASSWORD)
session.verify = False
session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

# (2) Make URL
url = 'https://{}:9440/PrismGateway/services/rest/v2.0/vms/'.format(IP)
# 'https://10.149.27.41:9440/PrismGateway/services/rest/v1/cluster'

# (3) Send request and get Response
response = session.get(url)

# (4) Check response code
print('Response Code: {}'.format(response.status_code))

# (5) Check response body
#print('Response Body:')
print(response.text)

d = json.loads(response.text)
print(d['entities'][0]['name'])
print(d['entities'][0]['uuid'])

url2 = 'https://{}:9440/api/nutanix/v2.0/snapshots'.format(IP)
resp = session.get(url2)
if resp.ok:
	print(resp.json())
else:
	print('@@@@')