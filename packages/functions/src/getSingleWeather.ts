import { DynamoDB } from "aws-sdk";
import { Table } from "sst/node/table";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();

export async function main(
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> {
  const weatherId = event.pathParameters && event.pathParameters.id
      ? event.pathParameters.id
      : null;
  const weatherItem = await dynamoDb.get({
    TableName: "sst-weather-crud-rest-api-ts-weatherDataSST",
    Key: {
      id: weatherId,
    },
  }).promise();
  console.log("hello world")
  return {
    statusCode: 200,
    body: JSON.stringify(weatherItem),
  };
}