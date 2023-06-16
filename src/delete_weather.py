import boto3
import json
import random
import os
from aws_lambda_powertools import Logger, Metrics, Tracer
from botocore.exceptions import ClientError


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
    except ClientError as err:
        logger.debug(f" failed to create weather item{err.response['Error']}")
    return {
        'statusCode' : 200,
        'body': "Weather Delete Succeessfull"
    }

