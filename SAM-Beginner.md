
# Building a Serverless REST API with SAM, PYTHON and API GATEWAY

## Problem Statement


In this project, we'll see how to build a serverless rest api using aws SAM to provision 
our infrastructure, api gateway for authorizing,authenticating and creating api endpoints and 
python for defining the content of our lambdas.

## Prerequisite
1. [AWS Account](https://aws.amazon.com/). Amazon Web Services (AWS) is the world's most comprehensive and broadly adopted cloud, offering over 200 fully featured services from data centers globally.
2. [AWS Command Line Interface (AWS CLI)](https://awscli.amazonaws.com/AWSCLIV2.msi). The AWS CLI provides direct access to the public APIs of AWS services. You can explore a service's capabilities with the AWS CLI, and develop shell scripts to manage your resources
3. [ AWS SAM CLI](https://github.com/aws/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi). AWS Serverless Application Model Command Line Interface, provides a Lambda-like execution environment that lets you locally build, test, and debug applications defined by SAM templates or through the AWS Cloud Development Kit (CDK)
4. [Python](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe). The programming language used in this project
5. [VS Code](https://code.visualstudio.com/download) or Your favourite text editor.


## AWS Services used
1. [AWS SAM ](https://aws.amazon.com/serverless/sam/) To define the infrastructure : The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines per resource, you can define the application you want and model it using YAML. There is no additional charge to use AWS SAM. You pay for the AWS resources created using SAM in the same manner as if you created them manually. You only pay for what you use, as you use it. There are no minimum fees and no required upfront commitments.
2. [Amazon Cognito](https://aws.amazon.com/cognito/): With Amazon Cognito, you can add user sign-up and sign-in features and control access to your web and mobile applications. This service is free for less than 50,000 MAUs(monthly active users)
3. [Amazon API Gateway](https://aws.amazon.com/api-gateway/):Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. With Amazon API Gateway, you only pay when your APIs are in use. There are no minimum fees or upfront commitments
4. [AWS Lambda](https://aws.amazon.com/lambda/) : AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers. You can trigger Lambda from over 200 AWS services and software as a service (SaaS) applications, and only pay for what you use. Cost of using lambda functions.
 ![](img/lp.png)


## Creating a SAM Project
1. To kick off your new SAM application,With just ```sam init``` command, you'll be on your way to a brand new directory and a set of default templates to work with.


```
projectName
├── event
    ├── events.json
├── hello_world
    ├── _init_.py
    ├── app.py
    ├── requirements.txt
├── test
├── __init__.py
├── samconfig.toml
├── README.md
└── template.yaml
```


**Let's take the default and give it a little shakeup modification**

Rename the hello_world folder to src.
you can delete all files except ```samconfig.toml``` and ```template.yaml```.


    projectName
    ├── src
    ├── samconfig.toml
    ├── README.md
    └── template.yaml

#### Libraries Used in this Project
1. [Boto3]() is the AWS SDK for Python. It provides a high-level, object-oriented API for interacting with AWS services.
2. [Json](https://docs.python.org/3/library/json.html). The json library can parse JSON from strings or files. The library parses JSON into a Python dictionary or list. It can also convert Python dictionaries or lists into JSON strings.
3. [Random](https://docs.python.org/3/library/random.html) library. Use to generate random numbers used as item's id.


## Create Lambda Function
The first lambda will be to ```create/insert``` an item.
In the ```src``` folder create file with name ```createWeatherHandler.py```

 Create a lambda handler function that is used to create items on dynamodb.

 A ```POST``` request is sent through an ```API``` that contains ```weather``` infomation in the body.


  ```python
    import boto3
    import json
    import random
    

    def createWeather(event, context):
        Weather = json.loads(event['body'])['Weather']
        id = str(random.randrange(100, 999))
        dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': id}, 'Weather': {'S': Weather}})
        return {
            'statusCode': 200,
            'body': 'Successfully inserted data!'
        }
  ```
##### Function Arguments
[Event](https://aws-lambda-for-python-developers.readthedocs.io/en/latest/02_event_and_context/)  is the data that's passed to the function upon execution.

[Context](https://aws-lambda-for-python-developers.readthedocs.io/en/latest/02_event_and_context/) is a Python objects that implements methods and has attributes. It's main role is to provide information about the current execution environment.

#### How item gets to the database(dynamodb)

   A ```POST``` request is sent through an ```API``` that contains ```weather``` information in the body which ```triggers``` the function to ```insert/create``` ```weather``` item in ```dynamodb```.

   ```python 
   Weather = json.loads(event['body'])['Weather']
   ```
   The above code extracts ```weather data``` into a variable ```weather```.

  ```python
   dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': id}, 'Weather': {'S': Weather}})
  ```  
  The code above creates the weather item in ```dynamodb``` and returns ```status code 200```


You can print out the ```event``` and the ```context``` to see their contents. (To see this when the api is invoke, open your AWS account and search for lambda, open the lambda function with the corresponding ```createWeather```, Click on ```monitor``` and click on ```Cloudwatch```)

3. Save your file and open ```template.yaml``` file

```yaml
Resources
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Prod

  CreateWeather:
    Type: AWS::Serverless::Function
    Description: 'Lambda function inserts data into DynamoDB table'
    Properties:
      FunctionName: CreateWeather
      Handler: createWeatherHandler.lambda_handler
      Runtime: python3.10
      CodeUri: src/
      Policies:
        DynamoDBCrudPolicy:
          TableName: !Ref DynamoDBTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /
            Method: POST
            RestApiId: !Ref MyApi
```
4. Configure dynamodb table in ```yaml``` by adding the code snippet bellow.
```yaml
  DynamoDBTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      TableName: WeatherData
```
## Get Weather Lambda Function
Create a new file ```getWeatherHandler.py``` in ```src``` folder and add the code bellow 

  ```python
    import boto3
    import json
    import random


    def getAllWeather(event, context):
      table = dynamodb.Table('WeatherData')
      response = table.scan(TableName='WeatherData')
      print(response)
      return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
      }
  ```

##### Adding the function in ```yaml``` 
```yaml
  GetWeatherFunction:
    Type: AWS::Serverless::Function
    Description: 'Lambda function inserts data into DynamoDB table'
    Properties:
      FunctionName: GetAllWeatherFunction
      Handler: getWeatherHandler.getAllWeather
      Runtime: python3.10
      CodeUri: src/
      Policies:
        DynamoDBCrudPolicy:
          TableName: !Ref DynamoDBTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /
            Method: GET
            RestApiId: !Ref MyApi
```
## Get Weather Lambda Function
Create a new file ```deleteWeatherHandler.py``` in ```src``` folder and add the code bellow 

```python

import boto3
import json
import random


def DeleteWeather(event, context):
    table = dynamodb.Table('WeatherData')
    key = json.loads(event['body'])['id']
    table.delete_item(
        Key = {
            "id": key
        }
    )
    return {
        'statusCode' : 200,
        'body': "Delete Succeessfull"
    }
  ```
##### Adding the function in ```yaml``` 
```yaml

  DeleteWeatherFunction:
    Type: AWS::Serverless::Function
    Description: 'Lambda function inserts data into DynamoDB table'
    Properties:
      FunctionName: DeleteWeatherFunction
      Handler: DeleteWeatherHandler.DeleteWeather
      Runtime: python3.10
      CodeUri: src/
      Policies:
        DynamoDBCrudPolicy:
          TableName: !Ref DynamoDBTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /
            Method: DELETE 
            RestApiId: !Ref MyApi 
 ```
## Update Weather Lambda Function
An item already registered in dynamodb can be update by providing its ```id``` and the ```attributes``` you want to update with new content.

Create a new file ```updateWeatherHandler.py``` in ```src``` folder and add the code bellow 


```python
import boto3
import json
import random


def updateWeather(event, context):
  Weather = json.loads(event['body'])['weather']
  key = json.loads(event['body'])['id']
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': key}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Data Updated Successfully!'
  }
  ```

Final Project folder structure

    projectName
    ├── src
        ├── createWeatherHandler.py
        ├── getWeatherHandler.py
        ├── deleteWeatherHandler.py
        ├── updateWeatherHandler.py
        ├── requirements.txt
    ├── samconfig.toml
    ├── README.md
    └── template.yaml

##### Building and Deploying the application

1.  Build your application. Use the ```sam build``` command to build your application. This will create a ZIP file that contains your application code and dependencies.
2.  Deploy your application. Use the ```sam deploy --guided``` command to deploy your application. This will create the AWS resources defined in your template and deploy your application code.


## Testing the end points

Open postman and send a post request to your end point.

![postman post request](img/postPostman.png)

Open postman and send a post request to your end point.

![postman post request](img/getPostman.png)

Currently, The endpoints we have can be accessed by any body and that is not what we want.
Lets add Authorization such that without the Cognito token, you cannot access our API's

## Adding Authorization with Cognito

To Add authorization with cognito follow the following steps.
1. Open your aws console and Create cognito user pool
2. Configure your ```template.yaml``` file
3. Add the below code to ```MyApi``` in the ```resources``` in your ```yaml file```
```yaml
      Cors: "'*'"
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: yourUserPoolArn
  ```


1. Add user cognito properties to the ```resources``` int the ```yaml file```

```yaml
  WeatherUserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !GetAtt UserPoolName
      Policies:
        PasswordPolicy:
          MinimumLength: 8
      UsernameAttributes:
        - email
      Schema:
        - AttributeDataType: String
          Name: email
          Required: false
  
  WeatherUserPoolClient:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      UserPoolId: !GetAtt userPoolId
      ClientName: !GetAtt clientName
      GenerateSecret: false     
```

Get the final template.yaml file [here]().

Run ```sam build``` to build your recent changes.

Run ```sam deploy``` to deploy your recent changes.

if you try to access your api again

![](img/postUnAuth.png)

![](img/getUnAuth.png)

To be able to access the api, do the following in postman

click on  ```authorization```

![](img/p1.png)

![](img/p2.png)

![](img/p3.png)

![](img/p4.png)

Now Click on the ```Generate```

Login Screen pops up.
Sign up with your email
![](img/c1.png)

Another screen with pop that contains the IdToken and AccessToken
![](img/t1.png)

![](img/t2.png)

Copy the IdToken and change the ```type``` to ```Bearee token``` 
![](img/b.png)

Paste the copied token on the space for ```Token```

Once you are done you can click on send.

![postman post request](img/postPostman.png)

Open postman and send a post request to your end point.

![postman post request](img/getPostman.png)

To Know more about cognito, click [here](https://github.com/vernyuy/intro_to_cognito/blob/main/cognito.md)

Reference

[Educloud](educloud.academy).

👍👏👍