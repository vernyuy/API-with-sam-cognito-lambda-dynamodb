import boto3
import json
import random
import os
from aws_lambda_powertools import Logger, Metrics, Tracer
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')

table_name = os.environ.get("TABLE_NAME")
logger = Logger()
metrics = Metrics()
Tracer = Tracer()

def lambda_handler(event, context):
  weather = json.loads(event['body'])['Weather']
  town = json.loads(event['body'])['town']
  id = str(random.randrange(100, 999))
  item = {
    'id': {'S': id}, 
    'Weather': {'S': weather},
    'Weather': {'S': town}
  }
  print(id)
  try:
    dynamodb_client.put_item(TableName=table_name, Item=item)
  except ClientError as err:
    logger.debug(f" failed to create weather item{err.response['Error']}")
  return {
      'statusCode': 200,
      'body': 'Successfully inserted data!'
  }
