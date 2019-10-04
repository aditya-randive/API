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

session = requests.Session()
session.auth = (USER, PASSWORD)
session.verify = False
session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks'.format(IP)
response = session.get(url)
if not response.ok:
	print(response.text)
	exit(1)

d = json.loads(response.text)
print(json.dumps(d,indent=2))

networks = d['entities']

# (1) HTTP GET : Read
for network in networks:
	print('(1) : HTTP GET : Get all network names')
	url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks'.format(IP)
	response = session.get(url)
	if not response.ok:
  		print(response.text)
  		exit(1)
	print(response.text)

# (2) HTTP Post : Create
print('(2) HTTP POST : Create Network')
url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks'.format(IP)
name = 'testNet'
vlan = '1234'
body_dict = {
	"name": name,
	"vlan_id": vlan
}
body_text = json.dumps(body_dict)

response = session.post(url, data=body_text)
if not response.ok:
	print('Response status has problem. Abort')
	print(response.status_code)
	print(response.text)
	exit(1)
print('Created New Network')

print('wait 30 secs')
print()


# (3) HTTP PUT : Update
print('(3) HTTP PUT : Update network via UUID')
# get uuid
url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks'.format(IP)
response = session.get(url)
if not response.ok:
  print(response.text)
  exit(1)
d = json.loads(response.text)

name = 'testNet'
uuid = ''
for network in d['entities']:
  if network['name'] == name:
    uuid = network['uuid']
if uuid == '':
  print('Unable to find network "{}"'.format(name))
  exit()

# update
url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks/{}'.format(IP, uuid)
body_dict = {
  'name': name,
  "vlan_id": '1111'
}
body_text = json.dumps(body_dict)
response = session.put(url, data=body_text)
if not response.ok:
  print(response.text)
  exit(1)
print('Updated Existing network')

print('wait 30 secs')
print()
time.sleep(30)


# (4) HTTP DELETE : Delete
print('(4) HTTP DELETE : Delete Network via UUID')
url = 'https://{}:9440/PrismGateway/services/rest/v2.0/networks/{}'.format(IP, uuid)
response = session.delete(url)
if not response.ok:
  print(response.text)
  exit(1)
print('Deleted network')
