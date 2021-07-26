import requests
import os
import json
import pymsteams

from dotenv import load_dotenv

load_dotenv()
username = os.environ.get('adsusername')
password = os.environ.get('adspassword')

myTeamsMessage = pymsteams.connectorcard("https://accenture.webhook.office.com/webhookb2/9489642d-1182-4190-92d5-60218c2e6aec@e0793d39-0939-496d-b129-198edd916feb/IncomingWebhook/e83ecca339aa421db3af0ddcd836c804/094b29e3-09c6-427c-a5c4-d56376c1376b")
myTeamsMessage.color("#00FF00")


auth_url = 'http://mn1gvwug0001:9644/api/v1/token'
auth_data = f'grant_type=password&username={username}&password={password}'
auth_headers = {
    "Content-Type":"application/json",
    "Accept":"application/json"
}
auth_reponse = requests.post(url=auth_url, data=auth_data, headers=auth_headers,verify=False).json()
#print(json.dumps(auth_reponse, indent=2))

token = auth_reponse['access_token']




base_url = 'http://mn1gvwug0001:9644/api/v1/'
req_headers = {
    "Content-Type":"application/json",
    "Accept":"application/json",
    "Authorization":f"Bearer {token}"
}

endpoint_deviceGrp = 'device-groups/0/devices'

get_url=f"{base_url}{endpoint_deviceGrp}"


deviceGrp_response = requests.get(url=get_url, headers=req_headers, verify=False).json()
devices = deviceGrp_response['data']['devices']
pageNo = deviceGrp_response['paging']['nextPageId']

for device in devices:
    if device['bestState'] == "Down":
        hostname = device['hostName']
        IPaddress = device['networkAddress']
        print(f"{hostname}({IPaddress}) is currently down! Please Check WUG Alert!!")    
        #myTeamsMessage.text(f"{hostname}({IPaddress}) is currently down! Please Check WUG Alert!!") 
        #myTeamsMessage.send()

while pageNo:
    deviceGrp_response = requests.get(url=get_url, headers=req_headers, params={"pageId":pageNo}, verify=False).json()
    devices = deviceGrp_response['data']['devices']

    for device in devices:
        if device['bestState'] == "Down":
            hostname = device['hostName']
            IPaddress = device['networkAddress']
            print(f"{hostname}({IPaddress}) is currently down! Please Check WUG Alert!!")   
            #myTeamsMessage.text(f"{hostname}({IPaddress}) is currently down! Please Check WUG Alert!!") 
            #myTeamsMessage.send()



    try:
        pageNo = deviceGrp_response['paging']['nextPageId']
        
    except:
        break

