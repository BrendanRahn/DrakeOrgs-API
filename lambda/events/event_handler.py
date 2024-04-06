import boto3
import json
import uuid
import re



def connect_dynamo(table_name):
     dynamo = boto3.resource('dynamodb')
     return dynamo.Table(table_name)

def post_event(event: dict):

    table = connect_dynamo("events")
    try:
        response = table.put_item(Item=event)
        return {
            "status": 200,
            "body": response
        }

    except Exception as error:
        return error



def get_all_events():

    table = connect_dynamo("events")
    response = table.scan()
    data = response["Items"]

    return {"status_code": 200,
            "body": json.dumps(data)}
    


def validate_event_data(body: dict):

    ########################
    if "title" not in body:
        return param_not_found("title")
    
    event_title = body["title"]
    if type(event_title) != str:
        return type_not_string("title")
    

    ##########################
    if "description" not in body:
        return param_not_found("description")
    
    event_description = body["description"]
    if type(event_description) != str:
        return type_not_string("description")
    



    ###########################
    if "date" not in body:
        return param_not_found("date")

    event_date = body["date"]
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
                "title": event_title,
                "description": event_description,
                "date": event_date
            }
        }
    

def type_not_string(parameter: str):
    return {
            "is_valid": False,
            "body": f"error, {parameter} is not of type string"
            }

def param_not_found(parameter: str):
    return {
            "is_valid": False,
            "body": f"error, {parameter} is not in format MM-DD-YYYY"
            }