# lambda function to get single item from dynamodb table
import json
import boto3
import os
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")


def lambda_handler(event, context):
    weather_id = str(json.loads(event['pathParameters'])['id'])
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={'id': weather_id})
        return json.dumps(response['Item'])
    except table_name:
        return {
            'statusCode': 500,
            'message': "Unable to get item"
        }