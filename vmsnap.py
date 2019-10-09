#ADITYA RANDIVE
#aditya.randive@nutanix.com

import sys
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
NTXPRISMCENTRAL = '10.45.140.160:9440'
NTXBASEURL3 = 'https://10.45.140.160:9440/api/nutanix/v3/idempotence_identifiers'
NTXBASEURL2 = 'https://{prismhost}/PrismGateway/services/rest/{version}/vms'.format(prismhost=NTXPRISMCENTRAL, version='v2.0')

testVM_UUID = '353b1148-7259-46ea-ba01-9e715ef4b378'

#testVMSnap_UUID = '825a454f-4311-4b6c-80a9-731c87591cb9'
#testVMSnap_UUID = '00000000-0000-0000-0000-000000000000'
# (3) Send request and get Response
#response3 = session.get(NTXBASEURL3)
#response2 = session.get(NTXBASEURL2)

# (4) Check response code

# (5) Check response body
#resp_var = json.loads(response2.text)
#print(resp_var['entities'][0]['name'])
#print(resp_var['entities'][0]['uuid'])
#=================================================================================================
# (6) VM Snapshots API
def getSingleVMSnapDetails(testVMSnap_UUID):
	getVMsnaps = 'https://{prismhost}/api/nutanix/v3/vm_snapshots/{uuid}'.format(prismhost = NTXPRISMCENTRAL, uuid = testVMSnap_UUID)
	getVMsnaps_response = session.get(getVMsnaps)
	print(getVMsnaps_response.text)
	z = json.loads(getVMsnaps_response.text)
	if getVMsnaps_response.ok:
		print(json.dumps(getVMsnaps_response.json(), indent = 2))
		#print(z['entities'][0]['vm_uuid'])
	else:
		print('ERROR: Could not get VM Snapshots')
#=================================================================================================
def createCrashConsistentVMS(entity_uuid, name, uuid):
	urlrun = 'https://{prismhost}/api/nutanix/{version}/vm_snapshots'.format(prismhost=NTXPRISMCENTRAL, version='v3')
	data = {
      "spec": {
        "resources": {
          "entity_uuid": testVM_UUID
        },
        "snapshot_type": "CRASH_CONSISTENT",
        "name": name
      },
      "api_version": "3.1",
      "metadata": {
        "kind": "vm_snapshot",
        "uuid": uuid
      }
    }
	createVM_response = session.post(urlrun, json=data)
	if createVM_response.ok:
		print(createVM_response.text)
		print("-------------------")
		print("Newly created Snap UUID: " + createVM_response.text)
		print("-------------------")
	else:
		print(createVM_response)
#=================================================================================================
def deleteVMS():
	urlrun = 'https://{prismhost}/api/nutanix/{version}/vm_snapshots/{uuid}'.format(prismhost=NTXPRISMCENTRAL, version='v3', uuid='a63b1c33-b349-4538-86b9-51e98c597fe2')
	delVM_response = session.delete(urlrun)
	print(delVM_response.text)
#=================================================================================================
def getIdentifier():
	urlrun = 'https://{prismhost}/api/nutanix/{version}/idempotence_identifiers/{id}'.format(prismhost=NTXPRISMCENTRAL, version='v3', id=testVMSnap_UUID)
	id_response = session.get(urlrun)
	print(id_response.text)
#=================================================================================================
def createSnapID(client_identifier, count=1):
	urlrun = 'https://{prismhost}/api/nutanix/{version}/idempotence_identifiers'.format(prismhost=NTXPRISMCENTRAL, version='v3')

	data = {
        "count": count,
        "client_identifier": client_identifier
	}
	snapID_response = session.post(urlrun, data=json.dumps(data))
	if snapID_response.ok:
		snapuuid = snapID_response.json()
            # return the unique element
		print(snapuuid.get('uuid_list', []))
	else:
		print("ERROR: SNAP ID could not be created")
#=================================================================================================
def listAllVMSnaps():
	urlrun = 'https://{prismhost}/api/nutanix/{version}/vm_snapshots/list'.format(prismhost=NTXPRISMCENTRAL, version='v3')

	data = {
        "filter": 'entity_uuid==' + testVM_UUID,
        "kind": "vm_snapshot"
	}

	listVMSnapsID_response = session.post(urlrun, data=json.dumps(data))
	if listVMSnapsID_response.ok:
		listVMSnapsID_details = listVMSnapsID_response.json()
            # return the unique element
		print(json.dumps(listVMSnapsID_details, indent = 2))
	else:
		print("ERROR: VM Snaps could not be listed")
#=================================================================================================
def main():
	print("IN MAIN")
	#createSnapID()
	#getIdentifier()
	#createCrashConsistentVMS()
	#getSingleVMSnapDetails()
	#listAllVMSnaps()
	#deleteVMS()

	method_name = "listAllVMSnaps"
	if not len(sys.argv) > 1:
		method_name = "listAllVMSnaps"
	else:
		method_name = sys.argv[1]

	if method_name == "getSingleVMSnapDetails":
		getSingleVMSnapDetails(*sys.argv[2:])
	elif method_name == "createCrashConsistentVMS":
		#parameter_name_1 = sys.argv[2]
		#parameter_name_2 = sys.argv[3]
		#parameter_name_3 = sys.argv[4]
		#getattr(sys.modules[__name__], method_name)(parameter_name_1, parameter_name_2, parameter_name_3)
		createCrashConsistentVMS(*sys.argv[2:])
	elif method_name == "createSnapID":
		createSnapID(*sys.argv[3:])
	else:
		listAllVMSnaps()

if __name__ == "__main__":
	main()