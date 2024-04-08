import boto3
import json
import uuid
import re



def connect_dynamo(table_name):
     dynamo = boto3.resource('dynamodb')
     return dynamo.Table(table_name)

def put_event(event: dict):


    table = connect_dynamo("events")
    try:
        response = table.put_item(Item=event)
        return {
            "status": 200,
            "body": "event posted successfully"
        }

    except Exception as error:
        return json.dumps(error.__dict__)



def get_all_events():

    table = connect_dynamo("events")
    response = table.scan()
    data = response["Items"]

    return json.dumps(data)
    


def validate_event_data(data: dict):

    
    ########################
    if "org-name" not in data:
        return param_not_found("org-name")
    
    org_name = data["org-name"]
    if type(org_name) != str:
        return type_not_string("org-name")
    
    
    ########################
    if "contact-name" not in data:
        return param_not_found("contact-name")
    
    contact_name = data["contact-name"]
    if type(contact_name) != str:
        return type_not_string("contact-name")
    
    
    ########################
    if "contact-email" not in data:
        return param_not_found("contact-email")
    
    contact_email = data["contact-email"]
    if type(contact_email) not in data:
        return type_not_string("contact-email")
    

    ########################
    if "title" not in data:
        return param_not_found("title")
    
    event_title = data["title"]
    if type(event_title) != str:
        return type_not_string("title")
    

    ##########################
    if "description" not in data:
        return param_not_found("description")
    
    event_description = data["description"]
    if type(event_description) != str:
        return type_not_string("description")
    

    ###########################
    if "location" not in data:
        return param_not_found("location")
    
    location = data["location"]
    if type(location) != str:
        return type_not_string("location")


    ###########################
    if "date" not in data:
        return param_not_found("date")

    event_date = data["date"]
    if type(event_date) != str:
        return type_not_string("date")
    
    if not re.match(r'^\d{2}-\d{2}-\d{4}$', event_date):
        return {
                "is_valid": False,
                "body": "error, date is not in format MM-DD-YYYY"
                }
    

    else:
        return {
            "is_valid": True,
            "body": {
                "org-name": org_name,
                "contact-name": contact_name,
                "contact-email": contact_email,
                "title": event_title,
                "description": event_description,
                "location": location,
                "date": event_date
            }
        }
    

def type_not_string(param_name: str, param_type: type):
    return {
            "is_valid": False,
            "body": f"error, {param_name} is of type {param_type}, not str"
            }

def param_not_found(parameter: str):
    return {
            "is_valid": False,
            "body": f"error, {parameter} not in data"
            }