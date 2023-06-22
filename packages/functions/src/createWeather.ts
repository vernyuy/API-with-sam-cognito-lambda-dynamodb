// import { DynamoDB } from "aws-sdk";
// import { Table } from "sst/node/table";

// const dynamoDb = new DynamoDB.DocumentClient();

// const putParams = {
//     TableName: "sst-weather-crud-rest-api-ts-weatherDataSST",
//     Key: {
//       id: "123",
//     }
//   };
//   await dynamoDb.update(putParams).promise();

import { DynamoDB } from "aws-sdk";
import { Table } from "sst/node/table";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();

export async function main(
  event: any
): Promise<APIGatewayProxyResult> {
  const weatherId = Math.floor(Math.random() * 1000).toString();
  const weather = JSON.parse(event.body).weather
  const town = JSON.parse(event.body).town
  JSON.parse(event.body).id = weatherId;

  const data = {
    id: weatherId,
    weather: weather,
    town: town
  }
  console.log("body", event.body)
  const response = await dynamoDb.put({Item: data, TableName: "sst-weather-crud-rest-api-ts-weatherDataSST"}).promise()

  console.log("response", response)
  if(response !== null) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        "message": "failed to create weather"
      })
    }
  }
  return {
    statusCode: 200,
    body: JSON.stringify({
        "message": "successfully created weather"
    }),
  };
}