import { DynamoDB } from "aws-sdk";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME as string
export async function main(
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> {
  const weatherId = event.pathParameters && event.pathParameters.id
      ? event.pathParameters.id
      : null;
  const weatherItem = await dynamoDb.get({
    TableName: tableName,
    Key: {
      id: weatherId,
    },
  }).promise();
  if (!weatherItem || !weatherItem.Item) {
    return{
      statusCode: 404,
      body: JSON.stringify({
        message: "No weather data found",
      }),
    }
  }
  return {
    statusCode: 200,
    body: JSON.stringify(weatherItem),
  };
}