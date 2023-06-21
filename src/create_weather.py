import json
import os
import random

import boto3

table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_data')


def lambda_handler(event, context):
    table = dynamodb.Table('weather_data')
    print(table_name)
    weather_id = str(random.randrange(100, 999))
    weather_name = json.loads(event['body'])['weather']
    weather_town = json.loads(event['body'])['town']
    item = { 
        "id": weather_id,
        "weather": weather_name,
        "town": weather_town
    }
    try:
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'meesage': 'Weather successfully created!'
        }
    except table_name:
        return {
            'statusCode': 500,
            'meesage': 'An error occured while creating the weather!'
        }
