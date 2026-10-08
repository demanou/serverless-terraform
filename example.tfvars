# Copy to terraform.tfvars and adjust. terraform.tfvars is git-ignored.
region             = "ca-central-1"
project_name       = "serverless-users"
environment        = "dev"
table_name         = "users"
lambda_timeout     = 10
lambda_memory_size = 128
log_level          = "INFO"
log_retention_days = 14
