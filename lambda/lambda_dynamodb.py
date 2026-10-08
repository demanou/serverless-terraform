import json
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
def create_table(tableName='users'):
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'last_name',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'last_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.wait_until_exists()

    return table

#  Creating a new item
def insert_item(table, username, first_name, last_name, age, account_type):
    table.put_item(
        Item={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'account_type': account_type,
            }
    )

# Updating an item
def update_item(table, username, last_name, age):
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

# Deleting an item
def delete_item(table, username, last_name):
    table.delete_item(
        Key={
            'username': username,
            'last_name': last_name
        }
    )

# Getting an item
def get_item(table, username, last_name):
    response = table.get_item(
        Key={
            'username': username,
            'last_name': last_name
        }
    )
    item = response['Item']
    return item

def lambda_handler(event, context):
    # TODO implement
    # table_name = event.get("Tablename", "No table name provided")

    # Create the DynamoDB table
    table_name = create_table()

    return {
        'statusCode': 200,
        'body': json.dumps('Table created!')
    }