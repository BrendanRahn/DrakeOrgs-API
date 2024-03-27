import boto3
import json

dynamo = boto3.resource('dynamodb')

def validate_lambda_event(event: dict):

    if "queryStringParameters" not in event:
            return {
                "is_valid": False,
                "body": "error, no parameters in url"
                }
    
    elif "org-name" not in event["queryStringParameters"]:
        return {
            "is_valid": False,
            "body": "error, org-name not in url parameters"
            }
    
    else:
        parameters = {
            "is_valid": True,
            "body": event["queryStringParameters"]["org-name"]
        }
        return parameters
    
def get_org_by_name(parameters: dict):

    table = dynamo.Table("student-org-data")
    key = {"org-name": parameters["org-name"]}
    data = table.get_item(Key=key)


    if data == None:
        return "it is null"


    return {
        'statusCode': '200',
        'body': json.dumps(data["Item"]) if "Item" in data else f'(error, item {key} not found)'
    }


def get_all_orgs():
    table = dynamo.Table("student-org-data")
    response = table.scan()
    data = response["Items"]
    return {
        "statusCode": "200",
        "body": json.dumps(data)
    }