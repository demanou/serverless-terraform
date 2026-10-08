variable "region" {
  type        = string
  default     = "ca-central-1"
  description = "AWS Region to deploy to"
}

variable "project_name" {
  type        = string
  default     = "serverless-users"
  description = "Prefix used to name resources"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment (dev, test, prod)"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be one of: dev, test, prod."
  }
}

variable "table_name" {
  type        = string
  default     = "users"
  description = "Name of the DynamoDB table"
}

variable "lambda_timeout" {
  type        = number
  default     = 10
  description = "Lambda timeout in seconds"
}

variable "lambda_memory_size" {
  type        = number
  default     = 128
  description = "Lambda memory in MB"
}

variable "log_level" {
  type        = string
  default     = "INFO"
  description = "Log level for the Lambda function (DEBUG, INFO, WARNING, ERROR)"
}

variable "log_retention_days" {
  type        = number
  default     = 14
  description = "How many days to keep Lambda logs in CloudWatch"
}
