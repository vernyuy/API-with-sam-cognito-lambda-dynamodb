from aws_cdk import Stack
from aws_cdk import aws_apigateway as _apigateway
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class CdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = _dynamodb.Table(self, "dynamodbTable", 
                                table_name="weather_data",
                                partition_key=_dynamodb.Attribute(name="id", type=_dynamodb.AttributeType.STRING))
        create_weather_lambda = _lambda.Function(self, "CreateWeatherLambdaFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler='create_weather.lambda_handler',
                                         code=_lambda.Code.from_asset('src'))
        get_weather_lambda = _lambda.Function(self, "GetWeatherLambdaFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler='get_weather.lambda_handler',
                                         code=_lambda.Code.from_asset('src'))
        update_weather_lambda = _lambda.Function(self, "UpdateWeatherLambdaFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler='update_weather.lambda_handler',
                                         code=_lambda.Code.from_asset('src'))
        delete_weather_lambda = _lambda.Function(self, "DeleteWeatherLambdaFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler='delete_weather.lambda_handler',
                                         code=_lambda.Code.from_asset('src'))
        get_single_weather_lambda = _lambda.Function(self, "GetSingleWeatherLambdaFunction",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler='get_single_weather.lambda_handler',
                                         code=_lambda.Code.from_asset('src'))
        weather_api = _apigateway.RestApi(
            self,
            'weather_rest_api'
        )
        table.grant_read_data(get_weather_lambda);
        table.grant_write_data(create_weather_lambda)
        table.grant_read_write_data(get_weather_lambda);
        table.grant_read_write_data(create_weather_lambda);
        table.grant_read_write_data(update_weather_lambda);
        table.grant_read_write_data(delete_weather_lambda);
        table.grant_read_data(get_single_weather_lambda);


        weather_api.root.add_resource("create-weather").add_method(
            "POST",
            _apigateway.LambdaIntegration(
                handler=create_weather_lambda
            )
        )
        weathers = weather_api.root.add_resource("weather")
        weathers.add_method(
            "GET",
            _apigateway.LambdaIntegration(
                handler=get_weather_lambda
            )
        )

        weather = weathers.add_resource('{id}')
        weather.add_method(
            "PUT",
            _apigateway.LambdaIntegration(
                handler=update_weather_lambda
            )
        )

        weather.add_method(
            "DELETE",
            _apigateway.LambdaIntegration(
                handler=delete_weather_lambda
            )
        )

        weather.add_method(
            "GET",
            _apigateway.LambdaIntegration(
                handler=get_single_weather_lambda
            )
        )