"""CRUD Lambda for the DynamoDB "users" table.

The function is invoked directly (console test event, AWS CLI or SDK) with an
"action" field: create, read, update or delete. See the events/ folder for
ready-to-use test events.
"""

import json
import logging
import os
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())

# The table name is injected by Terraform; "users" is kept as a fallback.
TABLE_NAME = os.environ.get("TABLE_NAME", "users")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


class ValidationError(Exception):
    """Raised when the incoming event is missing or has invalid fields."""


# ---------- helpers ----------

def _json_default(value):
    # DynamoDB returns numbers as Decimal, which json.dumps cannot serialize.
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def response(status_code, body):
    return {"statusCode": status_code, "body": json.dumps(body, default=_json_default)}


def require(event, *fields):
    missing = [f for f in fields if event.get(f) in (None, "")]
    if missing:
        raise ValidationError(f"Missing required field(s): {', '.join(missing)}")


def parse_age(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError("age must be a positive whole number")
    return value


def key_of(event):
    return {"username": event["username"], "last_name": event["last_name"]}


# ---------- CRUD operations ----------

def insert_item(event):
    require(event, "username", "first_name", "last_name", "age", "account_type")
    table.put_item(
        Item={
            "username": event["username"],
            "first_name": event["first_name"],
            "last_name": event["last_name"],
            "age": parse_age(event["age"]),
            "account_type": event["account_type"],
        },
        # Never overwrite an existing user by accident
        ConditionExpression="attribute_not_exists(username)",
    )
    return response(201, {"message": "Item inserted"})


def get_item(event):
    require(event, "username", "last_name")
    item = table.get_item(Key=key_of(event)).get("Item")
    if not item:
        return response(404, {"error": "Item not found"})
    return response(200, item)


def update_item(event):
    require(event, "username", "last_name", "age")
    table.update_item(
        Key=key_of(event),
        UpdateExpression="SET age = :age",
        ExpressionAttributeValues={":age": parse_age(event["age"])},
        # Only update users that already exist (no silent creation)
        ConditionExpression="attribute_exists(username)",
    )
    return response(200, {"message": "Item updated"})


def delete_item(event):
    require(event, "username", "last_name")
    table.delete_item(Key=key_of(event))
    return response(200, {"message": "Item deleted"})


ACTIONS = {
    "create": insert_item,
    "read": get_item,
    "update": update_item,
    "delete": delete_item,
}


# ---------- router ----------

def lambda_handler(event, context):
    action = event.get("action")
    logger.info("Received action=%s", action)

    handler = ACTIONS.get(action)
    if handler is None:
        return response(400, {"error": f"Invalid action. Use one of: {', '.join(ACTIONS)}"})

    try:
        return handler(event)
    except ValidationError as err:
        return response(400, {"error": str(err)})
    except ClientError as err:
        code = err.response["Error"]["Code"]
        if code == "ConditionalCheckFailedException":
            if action == "create":
                return response(409, {"error": "User already exists"})
            return response(404, {"error": "Item not found"})
        logger.exception("DynamoDB error")
        return response(500, {"error": "Internal error"})
