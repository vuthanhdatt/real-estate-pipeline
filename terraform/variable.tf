variable "s3_bucket" {
  description = "Bucket name for S3"
  type        = string
  default     = ""
}

variable "db_password" {
  description = "Password for Redshift DB"
  type        = string
  default     = ""
}

variable "db_username" {
  description = "Username for Redshift DB"
  type        = string
  default     = ""
}