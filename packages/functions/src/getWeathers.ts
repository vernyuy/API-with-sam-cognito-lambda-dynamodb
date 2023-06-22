import { DynamoDB } from "aws-sdk";
import { Table } from "sst/node/table";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();

export async function main(
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> {
  const weatherData = await dynamoDb.scan({ TableName: "sst-weather-crud-rest-api-ts-weatherDataSST" }).promise();
    // event.pathParameters && event.pathParameters.id
    //   ? await dynamoDb.get({
    //     TableName: "sst-weather-crud-rest-api-ts-weatherDataSST",
    //     // Get the row where the counter is called "hits"
    //     Key: {
    //       id: event.pathParameters.id,
    //     },
    //   }).promise
    //   : null;
  // const getParams = {
  //   // Get the table name from the environment variable
  //   TableName: "sst-weather-crud-rest-api-ts-weatherDataSST",
  //   // Get the row where the counter is called "hits"
  //   Key: {
  //     id: "124",
  //   },
  // };
  // const results = await dynamoDb.get(getParams).promise();

  // If there is a row, then get the value of the
  // column called "tally"
  let weatherItems = weatherData.Items;

  return {
    statusCode: 200,
    body: JSON.stringify(weatherItems),
  };
}