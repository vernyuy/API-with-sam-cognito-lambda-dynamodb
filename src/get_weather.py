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
  try:
    response = table.scan(TableName=table_name)
    return {
      'statusCode': 200,
      'body': json.dumps(response['Items'])
    }

  except ClientError as err:
    logger.debug(f" failed to get weather items{err.response['Error']}")
  print(response)
