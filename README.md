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



# TODO:
- Creat script for compressing lambda to zip file and uploading to AWS
- Make mounted volume for container so changes made to the lambda file(s) can be reflected in the container without reloading (need to make sure that is possible) 
