terraform {
    required_version = ">= 1.2.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.20.1"
        }
    }
}

provider "aws" {
  region  = "ap-southeast-1"
}


resource "aws_s3_bucket" "b" {
  bucket = var.s3_bucket
  force_destroy = true 
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}