import boto3
import json

print('Loading function')
dynamo = boto3.resource('dynamodb')



def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }



def get_dynamo(parameters: dict):
    
    table = dynamo.Table("student-org-data")
    key = {"org-name": parameters["org-name"]}
    data = table.get_item(Key=key)
    
    print(parameters)
    
    if data == None:
        return "it is null"
        
    print(data)
    
    
    return {
        'statusCode': '200',
        'body': json.dumps(data["Item"]) if "Item" in data else f'(error, item {key} not found)'
    }



def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    req_route_key = event["routeKey"] if "routeKey" in event else None

    if req_route_key == "GET /DrakeOrgs-API/ping":
        return "pong"

    if req_route_key == "GET /DrakeOrgs-API/get":

        #returns dict with relevant parameters for querying if valid,
        #otherwise returns str error message
        validation = validate_event(event)

        if type(validation) == dict:
            return get_dynamo(validation)
        else:
            return error_response(validation)
    

        
    else:
        return error_response(
            f'(error, path "{req_route_key}" not found. Ask Brendan to set up cloudwatch accounts for debugging)'
            )
        

def validate_event(event: dict):

    if "queryStringParameters" not in event:
            return "error, no parameters in url"
    
    elif "org-name" not in event["queryStringParameters"]:
        return "error, org-name not in url parameters"
    
    else:
        parameters = {
            "org-name": event["queryStringParameters"]["org-name"]
        }
        return parameters

def error_response(err: str):
    return {
        "statusCode": 400,
        "body": err
    }

