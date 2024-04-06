import json
import os

from .org_data import org_data_handler
from .events import event_handler



def lambda_handler(event, context):
    
    #print events for cloudwatch logs
    print("Received event: " + json.dumps(event, indent=2))


    #handle routes 
    req_route_key = event["routeKey"] if "routeKey" in event else None

    if req_route_key == "GET /DrakeOrgs-API/ping":
        return "pong"
    
    if req_route_key == "GET /DrakeOrgs-API/get/all":
        return org_data_handler.get_all_orgs()

    if req_route_key == "GET /DrakeOrgs-API/get":

        org_validation = org_data_handler.validate_org_request(event)

        if org_validation["is_valid"] == True:
            return org_data_handler.get_org_by_name(org_validation["body"])
        
        elif org_validation["is_valid"] == False:
            return error_response(org_validation["body"])
        

    if req_route_key == "GET /DrakeOrgs-API/events/get/all":
        return event_handler.get_all_events()
    
    if req_route_key == "POST /DrakeOrgs-API/events/post-event":
        #event data should be in the body of the post request
        event_validation = event_handler.validate_event_data(event["body"])
        if event_validation["is_valid"] == False:
            return error_response(event_validation["body"])
        
        elif event_validation["is_valid"] == True:
            return event_handler.post_event(event_validation["body"])


    else:
        return error_response(
            f'(error, path "{req_route_key}" not found. Check cloudwatch accounts for debugging)'
            )
        


def error_response(err: str):
    return {
        "statusCode": 400,
        "body": err
    }
