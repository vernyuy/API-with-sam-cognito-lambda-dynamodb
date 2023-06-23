import { Api, StackContext, Table } from "sst/constructs";

export function WeatherCrudStack({ stack }: StackContext) {
  // create the http api
  
  const table = new Table(stack, "weatherDataSST", {
    tableName: "weatherDataSST",
    fields: {
      id: "string",
    },
    primaryIndex: { partitionKey: "id" },
  });

  const api = new Api(stack, "api", {
    defaults: {
      function: {
        bind: [table]
      }
    },
    routes: {
      "post /weather": "packages/functions/src/createWeather.main",
      "get /weather": "packages/functions/src/getWeathers.main",
      "get /weather/{id}": "packages/functions/src/getSingleWeather.main",
      "put /weather/{id}": "packages/functions/src/updateWeather.main",
      "delete /weather/{id}": "packages/functions/src/deleteWeather.main",
    },
  });

  // show the api endpoint in the output
  stack.addOutputs({
    apiendpoint: api.url,
  });
}