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

#access_control_policy
resource "aws_s3_bucket_acl" "access" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.b.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Create S3 Read only access role.
resource "aws_iam_role" "redshift_role" {
  name = "RedShiftLoadRole"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

# Confuge security group for Redshift allowing all inbound/outbound traffic
 resource "aws_security_group" "sg_redshift" {
  name        = "sg_redshift"
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# Create Redshift cluster

resource "aws_redshift_cluster" "redshift" {
  cluster_identifier = "real-estate-pipeline"
  skip_final_snapshot = true 
  database_name = "cho_tot_db"
  master_username    = var.db_username
  master_password    = var.db_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = "true"
  iam_roles = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.sg_redshift.id]
  
}
