import { SSTConfig } from "sst";
import { WeatherCrudStack } from "./stacks/WeatherCrudStack";

export default {
  config(_input) {
    return {
      name: "weather-crud-sst",
      region: "eu-west-1",
    };
  },
  stacks(app) {
    app.stack(WeatherCrudStack);
  }
} satisfies SSTConfig;
