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

    #catch errors with formating
    event_title = body["title"]
    if type(event_title) != str:
        return {
                "is_valid": False,
                "body": "error, title is not of type string"
                }
    
    event_description = body["description"]
    if type(event_description) != str:
        return {
                "is_valid": False,
                "body": "error, description is not of type string"
                }
    
    event_date = body["date"]
    if type(event_date) != str:
        return {
                "is_valid": False,
                "body": "error, date is not of type string"
                }
    
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
    




    print("")