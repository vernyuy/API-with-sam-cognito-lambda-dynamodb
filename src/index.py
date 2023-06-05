# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
import random


def lambda_handler(event, context):
  Weather = json.loads(event['body'])['Weather']
  id = random.randrange(100, 999)
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': id}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Successfully inserted data!'
  }


def getWeather(event, context):
  table = dynamodb.Table('WeatherData')
  response = table.scan(TableName='WeatherData')
  return {
    'statusCode': 200,
    'body': response['Items']
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
        'message': "Delete Succeessfull"
    }


def updateWeather(event, context):
  Weather = json.loads(event['body'])['weather']
  key = json.loads(event['body'])['id']
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': key}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Data Updated Successfully!'
  }
