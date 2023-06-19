import boto3
import json
import os


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
  except:
    return {
      'statusCode': 500,
      'message': "Unable to get items"
    }
