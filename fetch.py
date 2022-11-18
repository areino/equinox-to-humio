import requests
import json
import datetime

## Equinox login info

email = ""
password = ""
plant = 

## Humio config

humio_hostname = "cloud.community.humio.com"
humio_token = ""


def log(s):
    print(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + '  ' + str(s))


## Authenticate to EQUINOX

log("Authenticating to Equinox")

url = "https://new-equinox.salicru.com/"
token = ""

headers =   {
            'Content-Type': 'application/json'
            }

data =      {  
            'email': email,
            'password': password,
            'appVersion': 'web'  
            }

response = requests.request(method = "POST", url = url + "users/login", data = json.dumps(data), headers = headers)

if response.status_code != 200:
    log("Error: " + response.content)
    exit(-1)


response = response.json()

token = response["token"]
userid  = response["userId"]

log("Successfully authenticated to Equinox with user " + userid + " (" + email + ")")

## Fetch real time data
log("Fetching real time status of plant " + str(plant))

headers =   {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
            }

response = requests.request(method = "GET", url = url + "plants/" + str(plant) + "/realTime", headers = headers)

if response.status_code != 200:
    log("Error: " + response.content)
    exit(-1)

telemetry = response.json()



## Upload to Humio

log("Sending telemetry to Humio")

headers =   {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + humio_token
            }

url = "https://" + humio_hostname + "/api/v1/ingest/raw"

response = requests.request(method = "POST", url = url, data = json.dumps(telemetry), headers = headers)

if response.status_code != 200:
    log("Error: " + response.content)
    exit(-1)

log("End")
