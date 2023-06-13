import boto3
import json
import random

dynamodb_client = boto3.client('dynamodb')


def updateWeather(event, context):
  Weather = json.loads(event['body'])['weather']
  key = json.loads(event['body'])['id']
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': key}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Data Updated Successfully!'
  }
