#Launching instance via lambda function

import json
import boto3

def lambda_handler(event, context):
    # Create EC2 client
    client = boto3.client('ec2')
    
    try:
        # Launch EC2 instance
        response = client.run_instances(
            ImageId='ami-0b7207e48d1b6c06f',  # Replace with the desired AMI ID
            InstanceType='t2.micro',  # Instance type
            KeyName='KEYPAIR',  # Replace with your EC2 key pair name
            MaxCount=1,
            MinCount=1
            # Omit 'SecurityGroupIds' and 'SubnetId' to use default security group and subnet
        )
        
        # Log the instance ID
        instance_id = response['Instances'][0]['InstanceId']
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"EC2 instance created successfully with ID: {instance_id}")
        }
    
    except Exception as e:
        # Error handling
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error launching EC2 instance: {str(e)}")
        }

