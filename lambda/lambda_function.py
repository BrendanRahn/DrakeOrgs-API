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

        validation = org_data_handler.validate_lambda_event(event)

        if validation["is_valid"] == True:
            return org_data_handler.get_org_by_name(validation["body"])
        
        elif validation["is_valid"] == False:
            return error_response(validation["body"])
        

    if req_route_key == "GET /DrakeOrgs-API/events/get/all":
        return event_handler.get_all_events()
    
    if req_route_key == "POST /DrakeOrgs-API/events/post-event":
        return "here"

    else:
        return error_response(
            f'(error, path "{req_route_key}" not found. Ask Brendan to set up cloudwatch accounts for debugging)'
            )
        


def error_response(err: str):
    return {
        "statusCode": 400,
        "body": err
    }
