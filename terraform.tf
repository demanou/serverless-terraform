terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.8"
    }
  }

  # Remote state in S3. Change the bucket to one you own before running
  # terraform init (or remove this block to use local state).
  backend "s3" {
    bucket = "dnag-s3-demo-bucket"
    key    = "env/dev/terraform-serverless.tfstate"
    region = "ca-central-1"
  }
}
