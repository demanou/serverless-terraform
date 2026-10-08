output "lambda_function_name" {
  description = "Name of the CRUD Lambda function"
  value       = aws_lambda_function.users_crud.function_name
}

output "lambda_function_arn" {
  description = "ARN of the CRUD Lambda function"
  value       = aws_lambda_function.users_crud.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.users.name
}

output "log_group_name" {
  description = "CloudWatch log group for the Lambda function"
  value       = aws_cloudwatch_log_group.lambda.name
}
