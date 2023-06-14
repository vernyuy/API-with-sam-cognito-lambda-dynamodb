import boto3
import json
import random

dynamodb = boto3.resource('dynamodb')

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

