# lambda function to update weather item in dynamodb
import json
import boto3
import os
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    weather = json.loads(event['body'])['weather']
    town = json.loads(event['body'])['town']
    print(event)
    key = str(json.loads(event['pathParameters'])['id'])
    item = {
        'id': key,
        'weather': weather,
        'town': town
    }
    try:
        table.update_item(TableName=table_name, Item=item)
        return {
            'statusCode': 200,
            'message': 'Weather Updated Successfully!'
        }
    except table_name:
        return {
            'statusCode': 500,
            'message': 'Ooops! An error occured.'
        }
