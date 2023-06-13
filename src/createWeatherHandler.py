import boto3
import json
import random

dynamodb_client = boto3.client('dynamodb')



def create_weather_handler(event, context):
  Weather = json.loads(event['body'])['Weather']
  id = str(random.randrange(100, 999))
  print(id)
  dynamodb_client.put_item(TableName='WeatherData', Item={'id': {'S': id}, 'Weather': {'S': Weather}})
  return {
      'statusCode': 200,
      'body': 'Successfully inserted data!'
  }
