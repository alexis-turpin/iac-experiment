# Variable declaration
variable "env" {
  default = "dev"
  description = "environnement to deploy (prod/staging/DEV)"
}

variable "aws_availability_zones" {
  type = "list"
  description = "All availability zones of the chosen Region"
}

variable "vpc_subnet_tag" {
  description = "Subnet used by the VPC 10.XXX.0.0/16 "
}
variable "front_subnet_tag" {
  description = "Subnet used by the front instances 10.vpc.X[1-9].0/16
  (recommended X < 10 in case the region has more than 10 AZ "
}
variable "back_subnet_tag" {
  description = "Subnet used by the back instances 10.vpc.X[1-9].0/16
  (recommended X < 10 in case the region has more than 10 AZ "
}
