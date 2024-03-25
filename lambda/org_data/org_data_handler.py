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