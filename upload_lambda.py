import boto3


def upload_lambda_package(function_name, zip_file_path):
    lambda_client = boto3.client("lambda")

    with open(zip_file_path, "rb") as zip_file:
        package_contents = zip_file.read()

    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name, ZipFile=package_contents
        )

        print(f"Lambda function {function_name} updated successfully.")
        print(f"Function ARN: {response['FunctionArn']}")
        print(f"Function Last Modified: {response['LastModified']}")

        return response
    except Exception as e:
        print(f"Error updating Lambda function: {str(e)}")
        return None


function_name = "LambdaTest"
zip_file_path = "aws_lambda/deployment_package.zip"

upload_lambda_package(function_name, zip_file_path)
