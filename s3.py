#create s3 bucket using boto3

import boto3
client=boto3.client('s3')
response = client.create_bucket(
    Bucket='qwertyuioasdfgh', #bucket name

    CreateBucketConfiguration={
        'LocationConstraint': "ap-south-1",
}
)
