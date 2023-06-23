import { DynamoDB } from "aws-sdk";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

const dynamoDb = new DynamoDB.DocumentClient();
const tableName = process.env.TABLENAME
export async function main(
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> {
  console.log(tableName)
  const weatherData = await dynamoDb.scan({ TableName: tableName }).promise();
  if(weatherData.Items == null)
    return {
      statusCode: 404,
      body: JSON.stringify({
        message: "No weather data found",
      }),
    }
  let weatherItems = weatherData.Items;
  
  return {
    statusCode: 200,
    body: JSON.stringify(weatherItems),
  };
}