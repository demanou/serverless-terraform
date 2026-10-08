locals {
  name_prefix   = "${var.project_name}-${var.environment}"
  function_name = "${local.name_prefix}-crud"
}

# ---------------------------------------------------------------------------
# DynamoDB table
# ---------------------------------------------------------------------------
resource "aws_dynamodb_table" "users" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "username"
  range_key = "last_name"

  attribute {
    name = "username"
    type = "S"
  }

  attribute {
    name = "last_name"
    type = "S"
  }

  # Point-in-time recovery (continuous backups) for production only.
  # Encryption at rest is on by default with an AWS owned key.
  point_in_time_recovery {
    enabled = var.environment == "prod"
  }
}

# ---------------------------------------------------------------------------
# IAM role for the Lambda function (least privilege)
# ---------------------------------------------------------------------------
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${local.name_prefix}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "lambda_permissions" {
  # Only the four actions the function uses, only on this table
  statement {
    sid    = "DynamoDBCrud"
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
    ]

    resources = [aws_dynamodb_table.users.arn]
  }

  # Write logs to this function's log group only
  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["${aws_cloudwatch_log_group.lambda.arn}:*"]
  }
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name   = "${local.name_prefix}-lambda-policy"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_permissions.json
}

# ---------------------------------------------------------------------------
# CloudWatch log group (created by Terraform so retention is controlled)
# ---------------------------------------------------------------------------
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = var.log_retention_days
}

# ---------------------------------------------------------------------------
# Lambda function
# ---------------------------------------------------------------------------
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda_dynamodb.py"
  output_path = "${path.module}/build/lambda_dynamodb.zip"
}

resource "aws_lambda_function" "users_crud" {
  function_name    = local.function_name
  description      = "CRUD operations on the ${var.table_name} DynamoDB table"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_dynamodb.lambda_handler"
  runtime          = "python3.13"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory_size

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.users.name
      LOG_LEVEL  = var.log_level
    }
  }

  # Make sure permissions and the log group exist before the function runs
  depends_on = [
    aws_iam_role_policy.lambda_permissions,
    aws_cloudwatch_log_group.lambda,
  ]
}

# ---------------------------------------------------------------------------
# Renamed resources: keep existing state instead of destroying/recreating
# ---------------------------------------------------------------------------
moved {
  from = aws_iam_role.example
  to   = aws_iam_role.lambda_exec
}

moved {
  from = aws_lambda_function.example
  to   = aws_lambda_function.users_crud
}

moved {
  from = aws_iam_role_policy.lambda_dynamodb_sns_full
  to   = aws_iam_role_policy.lambda_permissions
}
