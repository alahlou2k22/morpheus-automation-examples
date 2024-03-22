import requests, sys, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########
# Globals #
###########

VERBOSE = True

# Morpheus Globals
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 


#############
# Functions #
#############

configspec = morpheus['spec']

def getDatastoreId():
    cloudID=configspec['config']['customOptions']['cloud']
    sType=configspec['config']['customOptions']['storageType']
    # cloudID=morpheus['customOptions']['cloud']
    # sType=morpheus['customOptions']['storageType']
    sTypeCat = {
        "tccSilverLinux": "local",
        "tccPlatinumLinux": "ESXi-DC2-DEMO-LUN"
        }
    url="https://%s/api/zones/%s/data-stores" % (MORPHEUS_HOST,cloudID)
    response = requests.get(url, headers=MORPHEUS_HEADERS, verify=MORPHEUS_VERIFY_SSL_CERT)
    data = response.json()
    l = len(data['datastores'])
    dlist =[]
    dfreeSpace = []
    for i in range(0,l):
        dName = data['datastores'][i]['name']
        freeSpace = data['datastores'][i]['freeSpace']
        if sType in sTypeCat:
            if sTypeCat[sType] in dName:
                dlist.append(dName)
                dfreeSpace.append(freeSpace)
    dMaxFreeSpace = max(dfreeSpace)
    # print(dMaxFreeSpace)
    for i in range(0,l):
        if dMaxFreeSpace == data['datastores'][i]['freeSpace']:
            dMaxId = data['datastores'][i]['id']
    # print(dMaxId)
    # print(dMaxIdName)
    configspec['volumes'][0]['datastoreId'] = dMaxId
    newspec = {}
    newspec['spec'] = configspec
    print(json.dumps(newspec))

getDatastoreId()





