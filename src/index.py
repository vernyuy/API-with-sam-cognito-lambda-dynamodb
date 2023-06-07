# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import random
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')



def lambda_handler(event, context):
  print(event)
  print(context)
  Weather = json.loads(event['body'])['Weather']
  print(Weather)
  id = str(random.randrange(100, 999))
  print(id)
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': id}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Successfully inserted data!'
  }


def getWeather(event, context):
  table = dynamodb.Table('WeatherData')
  response = table.scan(TableName='WeatherData')
  print(response)
  return {
    'statusCode': 200,
    'body': json.dumps(response['Items'])
  }


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


def updateWeather(event, context):
  Weather = json.loads(event['body'])['weather']
  key = json.loads(event['body'])['id']
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': key}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Data Updated Successfully!'
  }
