import boto3
import json
import os


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    key = json.loads(event['pathParameters'])['id']
    id_key = {
        "id": key
    }
    print(event)
    try:
        table.delete_item(Key = id_key)
        return {
            'statusCode' : 200,
            'body': "Weather Delete Succeessfull"
        }
    except:
        return {
            'statusCode' : 500,
            'body': "An error occured. Weather not deleted"
        }
    

