provider "aws" {
  region = var.region

  # Tags applied automatically to every resource
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
