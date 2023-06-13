import boto3
import json
import random

dynamodb_client = boto3.client('dynamodb')

def getAllWeather(event, context):
  table = dynamodb.Table('WeatherData')
  response = table.scan(TableName='WeatherData')
  print(response)
  return {
    'statusCode': 200,
    'body': json.dumps(response['Items'])
  }

