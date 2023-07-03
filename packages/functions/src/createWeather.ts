import { DynamoDB } from "aws-sdk";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME as string
export async function main(
  event: any
): Promise<APIGatewayProxyResult> {
  const weatherId = Math.floor(Math.random() * 1000).toString();
  const weather = JSON.parse(event.body).weather
  const town = JSON.parse(event.body).town
  JSON.parse(event.body).id = weatherId;
  console.log("Hello sst")
  console.log(tableName)
  const params = {
    TableName: tableName,
    Item:{
      id: weatherId,
      weather: weather,
      town: town
    }
  }
  console.log("body", event.body)
  try{
  const response = await dynamoDb.put(params).promise()

  console.log("response", response)
  if(!response) {
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
}catch(err){
  console.log(err)
  return {
    statusCode: 500,
    body: JSON.stringify({
      "message": "failed to create weather"
    })
  }
}
}