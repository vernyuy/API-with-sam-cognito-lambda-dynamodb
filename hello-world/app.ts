import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient, BatchExecuteStatementCommand, GetItemCommand, PutItemCommand, QueryCommand, ScanCommand, DeleteItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({ region: "eu-west-1" });
const params = {
    TableName: 'sam12-ExampleTable-ZO12XPF44U3M',
    Key:{
        id: {
            S:"316"
        }
    }
}

export const lambdaHandler1 = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    let response: APIGatewayProxyResult;
    try {
        const test = await client.send(new ScanCommand({
            TableName: 'sam12-ExampleTable-4DPPPE0DQOO4'
        }))
        // console.log("Hello world",test)
        response = {
            statusCode: 200,
            body: JSON.stringify(test),
        };
    } catch (err: unknown) {
        console.log(err);
        response = {
            statusCode: 500,
            body: JSON.stringify({
                message: err instanceof Error ? err.message : 'some error happened',
            }),
        };
    }
    return response;
};
export const lambdaHandler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    let response: APIGatewayProxyResult;
    var blog_id = Math.floor(Math.random() * 1000).toString(); 
    console.log(event)
    console.log(event.body)
    // console.log(event['body'])
    var params = {
        "Item":{
            "id":{
                "S": blog_id
            },
            "title": {
                "S":  "event['title']"
            },
            "body": {
                "S":  "event['body']"
            }
        },
        "TableName": 'sam12-ExampleTable-4DPPPE0DQOO4',
        "ReturnConsumedCapacity": "TOTAL",
    };
    try {
        const test = await client.send(new ScanCommand({
            TableName: 'sam12-ExampleTable-4DPPPE0DQOO4'
        }))
        // console.log("Hello world",test)
        response = {
            statusCode: 200,
            body: JSON.stringify(test),
        };
    } catch (err: unknown) {
        console.log(err);
        response = {
            statusCode: 500,
            body: JSON.stringify({
                message: err instanceof Error ? err.message : 'some error happened',
            }),
        };
    }
    return response;
};


export const insertItem = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    let response: APIGatewayProxyResult;
    var blog_id = Math.floor(Math.random() * 1000).toString(); 
    console.log(event)
    console.log(event.body)
    // console.log(event['body'])
    var params = {
        "Item":{
            "id":{
                "S": blog_id
            },
            "title": {
                "S":  "event['title']"
            },
            "body": {
                "S":  "event['body']"
            }
        },
        "TableName": 'sam12-ExampleTable-4DPPPE0DQOO4',
        "ReturnConsumedCapacity": "TOTAL",
    };
    try {
        const test = await client.send(new PutItemCommand(params))
        // console.log("Hello world",test)
        response = {
            statusCode: 200,
            body: JSON.stringify({
                message: 'Inserted Successfully',
            }),
        };
    } catch (err: unknown) {
        console.log(err);
        response = {
            statusCode: 500,
            body: JSON.stringify({
                message: err instanceof Error ? err.message : 'some error happened',
            }),
        };
    }
    return response;
};


export const deleteItem = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    let response: APIGatewayProxyResult;
    try {
        const test = await client.send(new DeleteItemCommand({
            TableName: 'sam12-ExampleTable-4DPPPE0DQOO4',
            Key:{
                id:{
                    "S":'125'
                }
            }
        }))
        response = {
            statusCode: 200,
            body: JSON.stringify(
                {
                    message: 'Item deleted successfully',
                }
            ),
        };
    } catch (err: unknown) {
        console.log(err);
        response = {
            statusCode: 500,
            body: JSON.stringify({
                message: err instanceof Error ? err.message : 'some error happened',
            }),
        };
    }
    return response;
};
