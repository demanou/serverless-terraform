"""Standalone example: publish a message to an SNS topic.

This function is NOT deployed by the Terraform code in this repository.
Set the TOPIC_ARN environment variable on the function before testing.

Test event:  {"Message": "Hello from Lambda"}
"""

import json
import os

import boto3

client = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]  # e.g. arn:aws:sns:ca-central-1:<account-id>:TestLambda


def lambda_handler(event, context):
    message = event.get("Message", "No message provided")
    client.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject="Email from AWS",
    )
    return {
        "statusCode": 200,
        "body": json.dumps("Message delivered!"),
    }
