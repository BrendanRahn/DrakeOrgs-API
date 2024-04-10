import json
import os

from .org_data import org_data_handler
from .events import event_handler



def lambda_handler(event, context):
    
    #print events for cloudwatch logs
    print("Received event: " + json.dumps(event, indent=2))


    #handle routes 
    req_route_key = event["routeKey"] if "routeKey" in event else None

    match req_route_key:
        
        case "GET /DrakeOrgs-API/ping":
            return "pong"

        case "GET /DrakeOrgs-API/get/all":
            return org_data_handler.get_all_orgs()

        case "GET /DrakeOrgs-API/get":
            org_validation = org_data_handler.validate_org_request(event)

            if org_validation["is_valid"] == True:
                return org_data_handler.get_org_by_name(org_validation["body"])
            
            elif org_validation["is_valid"] == False:
                return error_response(org_validation["body"])
        
        case "GET /DrakeOrgs-API/events/get/all":
            return event_handler.get_all_events()

        case "PUT /DrakeOrgs-API/events/put-event":
            

            #api gateway passes body as a json-formatted string, convert with json.loads()
            json_body = json.loads(event["body"])
            

            event_validation = event_handler.validate_event_data(json_body["data"])

            if event_validation["is_valid"] == False:
                return error_response(event_validation["body"])
            
            elif event_validation["is_valid"] == True:
                return event_handler.put_event(event_validation["body"])
            

        #not an api route, this is triggered every 24hours by an EventBridge scheduler
        case "DEL /expired-events":
            print("get date")
        

        case _ :
            return error_response(
            f'(error, path "{req_route_key}" not found. Check cloudwatch accounts for debugging)'
            )

        


def error_response(err: str):
    return {
        "statusCode": 400,
        "body": err
    }
