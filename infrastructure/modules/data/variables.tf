variable "allocated_storage" {
  default     = 5
  description = "Allocated storage to the DB (5GB default)"
}

variable "instance_class" {
  default     = "db.t2.micro"
  description = "Instance hosting the DB (default db.t2.micro)"
}

variable "env" {
  default     = "dev"
  description = "prod/staging/DEV"
}

variable "db_password" {
  default     = "Password01"  #TODO: change
  description = "DB password"
}

variable "subnets_id" {
  type        = "list"
  description = "subnets ID in which to add the deployed instances"
}

variable "cidr_blocks" {
  type        = "list"
  description = "CIDR of subnet that can access the DB"
}

variable "vpc_id" {
  description = "VPC id where to create the db sg"
}
