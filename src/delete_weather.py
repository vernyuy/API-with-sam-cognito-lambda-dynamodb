import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")


def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    weather_id = str(json.loads(event['pathParameters'])['id'])
    id_key = {
        "id": weather_id
    }
    print(event)
    try:
        table.delete_item(Key=id_key)
        return {
            'statusCode': 200,
            'body': "Weather Delete Succeessfull"
        }
    except table_name:
        return {
            'statusCode': 500,
            'body': "An error occured. Weather not deleted"
        }
