# DrakeOrgs-API
Repo for the DrakeOrgs-API lambda function

# Requirements
- Docker
- AWS access key
    The lambda running in the container will still hit the AWS services hosted in the cloud. To allow authorization, you must pass in an AWS Access Key and Secret Key to environment variables in the docker container that the lambda can access. 

    Note: You can create an access key in the IAM service in AWS

    To do this, create a .env file ("code .env" in a cli) in the root directory of this repo, and add the variables in the following format:
        AWS_ACCESS_KEY_ID="your access key"
        AWS_SECRET_ACCESS_KEY="your secret key"
        AWS_DEFAULT_REGION="us-east-1" #(this one isnt a secret but still needs to be an env variable)

    You must do this before running the following steps to set up the container

    Note: The .env file is listed in the .gitignore file so it will not be uploaded to github with your access credentials. (This is why it is not a default part of the repo)


# Creating container
The lambda can be locally tested inside a docker container (yay!)
-First, build the docker image from the Dockerfile by running the command
    "docker build -t lambda_image ."
    this will build the image with the tag "lambda_image, which is used in the docker compose

-Second, build and run the docker container with the command
    "docker compose up"

This should create a running container hosting the lambda

# Local testing
The container hosts a server that run the AWS lambda Runtime Interface Client, which takes incoming network requests and passes them to the lambda as an event. 

The lambda can be invoked by making a request to the URL "http://localhost:9000/2015-03-31/functions/function/invocations", and passing the required arguments as in json format as the request body.

Tests have been written in the /tests folder in the repo that use the python requests library to hit the lambda with tests


# PUT event
Events will be posted to the events table in dynamodb. Events will be have to be sent from the app
as a PUT request to https://d4kfv1hyq7.execute-api.us-east-1.amazonaws.com/DrakeOrgs-API/events/put-event
with the event data in the format of a dictionary in the body of the put request. The format of the request from the app is as follows:

-(put body): {

    "data": {
        "org-name": "org name" (string)
        "contact-name": "contact name" (string)
        "contact-email" "contact email" (string)
        "title": "event-title" (string)
        "description": "description" (string)
        "location": "event location" (string)
        "date": "MM-DD-YY" (string) (must be in specified format)
    }
}

Notes:
- Currently the event title is the primary key in the dynamo table, any put requests with the same title will overwrite the current entry in the table
- pros:
- - if there is an error and multiple requests end up getting sent with the same info, this will prevent duplicate records
- cons:
- - How often will there be events from different orgs with the same title (one would overwrite the other) (-this is probably a dealbreaker)
 - - solution: make composite key with event id (add uuid in api handling)

# GET events
A list of all events can be requested at 
https://d4kfv1hyq7.execute-api.us-east-1.amazonaws.com/DrakeOrgs-API/events/get/all


# TODO:
