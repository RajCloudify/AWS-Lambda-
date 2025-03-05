#To create a AWS Lambda Function 
#Note:- It will create a lambda function and and add the function from the zip file in S3 bucket it won't upload the zip file in S3. The zip file should already be present in S3

import boto3

lambda_client = boto3.client('lambda', region_name='ap-south-1')

response = lambda_client.create_function(
    Code={
        'S3Bucket': 'rajsbbuckett',
        'S3Key': 'lambda.zip',  # Use the name of your ZIP file
    },
    Description='Process image objects from Amazon S3.',
    FunctionName="check-lambda",
    Handler='lambda-function.lambda_handler',
    Publish=True,
    Role='arn:aws:iam::703671931980:role/lambda-admin',
    Runtime='python3.12'
)
