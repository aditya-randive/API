#ADITYA RANDIVE
#aditya.randive@nutanix.com

import time
import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

IP = '10.45.140.160'
USER = 'admin'
PASSWORD = 'Nutanix.123'

# (1) Make Session
session = requests.Session()
session.auth = (USER, PASSWORD)
session.verify = False
session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

# (2) Make URL
#url = 'https://{}:9440/api/nutanix/v3'.format(IP)
NTXPRISMCENTRAL = '10.45.140.160:9440'
NTXBASEURL3 = 'https://{prismhost}/PrismGateway/services/rest/{version}/vms/list'.format(prismhost=NTXPRISMCENTRAL, version='v3')
NTXBASEURL2 = 'https://{prismhost}/PrismGateway/services/rest/{version}/vms'.format(prismhost=NTXPRISMCENTRAL, version='v2.0')

# (3) Send request and get Response
response3 = session.get(NTXBASEURL3)
response2 = session.get(NTXBASEURL2)

# (4) Check response code
print("================")
print('Response Code: {}'.format(response2.status_code))
print("================")

# (5) Check response body
#print('Response Body:')
#print(response.text)
resp_var = json.loads(response2.text)
print(resp_var['entities'][0]['name'])
print(resp_var['entities'][0]['uuid'])

# (6) Get VM Snapshots
def getVMS():
	getVMsnaps = 'https://{}:9440/api/nutanix/v2.0/snapshots'.format(IP)
	getVMsnaps_response = session.get(getVMsnaps)
	z = json.loads(getVMsnaps_response.text)
	if getVMsnaps_response.ok:
		print(json.dumps(getVMsnaps_response.json(), indent = 2))
		#print(z['entities'][0]['vm_uuid'])
	else:
		print('ERROR: Could not get VM Snapshots')

def getPDlist():
	urlrun = 'https://{prismhost}/PrismGateway/services/rest/{version}/{api}'.format(prismhost=NTXPRISMCENTRAL, version='v2.0', api='protection_domains/testPD/dr_snapshots')
	pd_response = session.get(urlrun)
	print(json.dumps(pd_response.json(), indent=4))

def createVMS():
	urlrun = 'https://{prismhost}/PrismGateway/services/rest/{version}/{api}'.format(prismhost=NTXPRISMCENTRAL, version='v2.0', api='snapshots')
	data = {
            "snapshot_specs": [
                {
                    "snapshot_name": "mySnapFunction",
                    "vm_uuid": "353b1148-7259-46ea-ba01-9e715ef4b378"
                }
            ]
        }

	createVM_response = session.post(urlrun, json = data)
	if createVM_response.ok:
		print(createVM_response.text)
		print("-------------------")
		print("Newly created Snap UUID: " + createVM_response.json()['task_uuid'])
		print("-------------------")
	else:
		print(createVM_response)

def deleteVMS():
	#aadf42cc-51ba-4017-b07e-aa1e5d46cb06
	urlrun = 'https://{prismhost}/PrismGateway/services/rest/{version}/snapshots/{uuid}'.format(prismhost=NTXPRISMCENTRAL, version='v2.0', uuid='aadf42cc-51ba-4017-b07e-aa1e5d46cb06')
	delVM_response = session.delete(urlrun)
	print(delVM_response.text)


def main():
	print("IN MAIN")
	#getVMS()
	createVMS()
	#deleteVMS()
    #getPDlist()
  
if __name__ == "__main__":
	main()
