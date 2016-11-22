# Variable declaration
variable "infra" {
  description = "Name of this deployment (front/back)"
}

variable "env" {
  default     = "dev"
  description = "environnement to deploy (prod/staging/DEV)"
}

variable "user_data" {
  description = "Script used to configure the aws launch configuration"
}

variable "key_name" {
  default     = "Alex-default"
  description = "Key used to access instance through SSH"
}

variable "min_size" {
  description = "Minimum size of AWS autoscaling group"
}

variable "max_size" {
  description = "Maximum size of AWS autoscaling group"
}

variable "instance_type" {
  description = "base instance to deploy"
  default     = "t2.micro"
}

variable "instance_port" {
  default     = "8080"
  description = "Port used by instance servers for http requests"
}

variable "open_port" {
  type        = "list"
  default     = [53, 80, 443]
  description = "WAN port to open (default to DNS53, HTTP80 and HTTPS443)"
}

variable "elb_port" {
  default     = 80
  description = "Port used by outside services to access infra described in this module"
}

variable "subnets_id" {
  type        = "list"
  description = "subnets ID in which to add the deployed instances"
}

variable "vpc_id" {
  description = "main vpc id, used to create security group"
}

variable "sg_internal_ssh_id" {
  description = "ID of the security group allow ssh connections between all my instance"
}

variable "aws_availability_zones" {
  type        = "list"
  description = "List of available AZ in my region"
}

variable "rds_access" {
  default     = false
  description = "should this module implementation have access to the database"
}

variable "sg_rds_id" {
  default     = ""
  description = "Security group applied to the database to access"
}
