import { DynamoDB } from "aws-sdk";
import { Table } from "sst/node/table";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();

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
  }

  if (event.body) {
    const data = {
      id: weatherId,
      weather: JSON.parse(event.body).weather?JSON.parse(event.body).weather: null,
      town: JSON.parse(event.body).town?JSON.parse(event.body).town: null,
    };

    const res = dynamoDb.put({TableName:'sst-weather-crud-rest-api-ts-weatherDataSST', Item: data}).promise()
    return {
      statusCode: 200,
      body: JSON.stringify({
        "message": "Weather updated successfully"
      }),
    };
  }

  return {
    statusCode: 500,
    body: JSON.stringify({
      "message": "Weather failed to update"
    }),
  };
}