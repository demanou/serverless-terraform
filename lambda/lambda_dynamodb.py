import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')   # La table doit être créée par Terraform

# CREATE
def insert_item(username, first_name, last_name, age, account_type):
    table.put_item(
        Item={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'account_type': account_type,
        }
    )
    return {"message": "Item inserted"}

# READ
def get_item(username, last_name):
    response = table.get_item(
        Key={
            'username': username,
            'last_name': last_name
        }
    )
    return response.get("Item", {})

# UPDATE
def update_item(username, last_name, age):
    table.update_item(
        Key={
            'username': username,
            'last_name': last_name
        },
        UpdateExpression='SET age = :val1',
        ExpressionAttributeValues={
            ':val1': age
        }
    )
    return {"message": "Item updated"}

# DELETE
def delete_item(username, last_name):
    table.delete_item(
        Key={
            'username': username,
            'last_name': last_name
        }
    )
    return {"message": "Item deleted"}

# ROUTER
def lambda_handler(event, context):

    action = event.get("action")

    if action == "create":
        return {
            "statusCode": 200,
            "body": json.dumps(
                insert_item(
                    event["username"],
                    event["first_name"],
                    event["last_name"],
                    event["age"],
                    event["account_type"]
                )
            )
        }

    elif action == "read":
        return {
            "statusCode": 200,
            "body": json.dumps(
                get_item(
                    event["username"],
                    event["last_name"]
                )
            )
        }

    elif action == "update":
        return {
            "statusCode": 200,
            "body": json.dumps(
                update_item(
                    event["username"],
                    event["last_name"],
                    event["age"]
                )
            )
        }

    elif action == "delete":
        return {
            "statusCode": 200,
            "body": json.dumps(
                delete_item(
                    event["username"],
                    event["last_name"]
                )
            )
        }

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid action"})
        }
