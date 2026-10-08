variable "region" {
  type        = string
  default     = "ca-central-1"
  description = "Enter Your Region Name"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.80.0.0/16"
  description = "Enter Your VPC CIDR"
}

variable "subnet1_cidr" {
  type        = string
  default     = "10.80.1.0/24"
  description = "Enter Your Subnet1 CIDR"
}

variable "subnet2_cidr" {
  type        = string
  default     = "10.80.2.0/24"
  description = "Enter Your Subnet2 CIDR"
}

variable "subnet3_cidr" {
  type        = string
  default     = "10.80.3.0/24"
  description = "Enter Your Subnet3 CIDR"
}

variable "subnet4_cidr" {
  type        = string
  default     = "10.80.4.0/24"
  description = "Enter Your Subnet4 CIDR"
}

variable "az1" {
  type        = string
  default     = "ca-central-1a"
  description = "Enter Your AZ1 Name"
}

variable "az2" {
  type        = string
  default     = "ca-central-1b"
  description = "Enter Your AZ2 Name"
}

variable "alb_sg_name" {
  type        = string
  default     = "metroc-alb-sg"
  description = "Enter Your ALB SG name"
}

variable "ec2_sg_name" {
  type        = string
  default     = "metroc-ec2-sg"
  description = "Enter Your EC2 SG name"
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
