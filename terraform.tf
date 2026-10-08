terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }
  backend "s3" {
    bucket = "dnag-s3-demo-bucket"
    key    = "env/dev/terraform-serverless.tfstate"
    region = "ca-central-1"
  }

  required_version = ">= 1.2"
}