import boto3
import json
import os
from aws_lambda_powertools import Logger, Metrics, Tracer
from botocore.exceptions import ClientError


dynamodb_client = boto3.client('dynamodb')
table_name = os.environ.get("TABLE_NAME")


def lambda_handler(event, context):
  weather = json.loads(event['body'])['weather']
  town = json.loads(event['body'])['town']
  print(event)
  key = json.loads(event['pathParameters'])['id']
  item={
    'id': {'S': key}, 
    'Weather': {'S': weather},
    'Town': {'S': town}
  }
  try:
    dynamodb_client.put_item(TableName=table_name, Item=item)
  except ClientError as err:
    logger.debug(f" failed to create weather item{err.response['Error']}")
  return {
      'statusCode': 200,
      'body': 'Weather Updated Successfully!'
  }
