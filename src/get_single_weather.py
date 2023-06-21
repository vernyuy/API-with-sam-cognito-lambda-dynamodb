import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")


def lambda_handler(event, context):
    weather_id = json.loads(event['pathParameters'])['id']
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={'id': weather_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    except table_name:
        return {
            'statusCode': 500,
            'message': "Unable to get item"
        }
