import { DynamoDB } from "aws-sdk";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();
const tableName = process.env.TABLENAME
export async function main(
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> {
  const weatherId =
    event.pathParameters && event.pathParameters.id
      ? event.pathParameters.id
      : null;

  if (!weatherId) {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: true }),
    };
  }else{
    dynamoDb.delete({TableName:tableName, Key:{
        id: weatherId
    }}).promise()
    return {
      statusCode: 200,
      body: JSON.stringify({
        "message": "Weather deleted successfully"
      }),
    };
  }
}