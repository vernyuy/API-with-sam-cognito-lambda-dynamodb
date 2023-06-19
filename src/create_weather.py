import boto3
import json
import random
import os

dynamodb_client = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
  weather = json.loads(event['body'])['Weather']
  town = json.loads(event['body'])['town']
  id = str(random.randrange(100, 999))
  item = {
    'id': id, 
    'weather': weather,
    'town': town
  }
  try:
    dynamodb_client.put_item(TableName=table_name, Item=item)
    return {
      'statusCode': 200,
      'meesage': 'Weather successfully created!'
    }
  except:
    return {
        'statusCode': 500,
        'message': 'Failed to create weather'
    }
