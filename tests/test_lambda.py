#will make http requests to docker container to hit the lambda with an event
#docker container must be running before funning tests

import requests
import json


CONTAINER_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def ping():
    event = json.dumps({
            "routeKey": "GET /DrakeOrgs-API/ping"
        })

    response = requests.post(
        CONTAINER_URL,
        data=event
    )
    return response.text

def test_get_org():
    event = json.dumps({
            "routeKey": "GET /DrakeOrgs-API/get",
            "queryStringParameters": {
                "org-name": "Best Buddies"
            }
        })
    
    response = requests.get(
        CONTAINER_URL,
        data=event
    )

    return response.text

def test_get_all():
    event = json.dumps({
            "routeKey": "GET /DrakeOrgs-API/get/all"
        })
    
    response = requests.get(
        CONTAINER_URL,
        data=event
    )

    return response.text

def test_get_all_events():
    event = json.dumps({
        "routeKey": "GET /DrakeOrgs-API/events/get/all"
    })

    response = requests.get(
        CONTAINER_URL,
        data=event
    )

    return response.text

# print(ping())
# print(test_get_org())
# print(test_get_all())

print(test_get_all_events()) 
