import boto3
import json



def connect_dynamo(table_name):
     dynamo = boto3.resource('dynamodb')
     return dynamo.Table(table_name)

# def post_event(event: dict):


    

    

def get_all_events():

    table = connect_dynamo("events")
    response = table.scan()
    data = response["Items"]

    return {"status_code": 200,
            "body": json.dumps(data)}
    

    

#
def validate_event_data(data: dict):
    



    print("")