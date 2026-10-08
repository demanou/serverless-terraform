import json
import boto3

client = boto3.client('sns')

def lambda_handler(event, context):
    # TODO implement
    message = event.get("Message", "No message provided")
    response = client.publish(
        TopicArn='arn:aws:sns:ca-central-1:962500058125:TestLambda',
        # PhoneNumber='string',
        Message=message,
        Subject='Email from AWS'
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Message delivered!')
    }
