"""Unit tests for lambda/lambda_dynamodb.py.

DynamoDB is simulated with moto, so the tests run without an AWS account.
Run with:  pytest
"""

import importlib
import json
import os
import pathlib
import sys

import boto3
import pytest
from moto import mock_aws

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lambda"))
EVENTS = ROOT / "events"


def load_event(name):
    return json.loads((EVENTS / f"{name}.json").read_text())


@pytest.fixture
def fn(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ca-central-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("TABLE_NAME", "users")
    with mock_aws():
        boto3.client("dynamodb").create_table(
            TableName="users",
            BillingMode="PAY_PER_REQUEST",
            KeySchema=[
                {"AttributeName": "username", "KeyType": "HASH"},
                {"AttributeName": "last_name", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "username", "AttributeType": "S"},
                {"AttributeName": "last_name", "AttributeType": "S"},
            ],
        )
        import lambda_dynamodb
        yield importlib.reload(lambda_dynamodb)  # reload so it binds to the mocked table


def call(fn, event):
    res = fn.lambda_handler(event, None)
    return res["statusCode"], json.loads(res["body"])


def test_full_crud_flow_with_sample_events(fn):
    assert call(fn, load_event("create"))[0] == 201

    status, item = call(fn, load_event("read"))
    assert status == 200
    assert item["first_name"] == "Jane" and item["age"] == 25  # Decimal serialized correctly

    assert call(fn, load_event("update"))[0] == 200
    assert call(fn, load_event("read"))[1]["age"] == 30

    assert call(fn, load_event("delete"))[0] == 200
    assert call(fn, load_event("read"))[0] == 404


def test_create_duplicate_returns_409(fn):
    call(fn, load_event("create"))
    assert call(fn, load_event("create"))[0] == 409


def test_update_missing_user_returns_404(fn):
    assert call(fn, load_event("update"))[0] == 404


def test_missing_fields_return_400(fn):
    status, body = call(fn, {"action": "create", "username": "janedoe"})
    assert status == 400
    assert "first_name" in body["error"]


@pytest.mark.parametrize("age", ["30", -1, 2.5, True])
def test_invalid_age_returns_400(fn, age):
    event = {**load_event("create"), "age": age}
    assert call(fn, event)[0] == 400


def test_invalid_action_returns_400(fn):
    assert call(fn, {"action": "drop"})[0] == 400
