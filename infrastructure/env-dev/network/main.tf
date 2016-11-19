# Get the data from remote state and amazon
data "aws_availability_zones" "all" {}

provider "aws" {
  region = "${var.region}"
}

module "network" {
  source = "../../modules/network"

  env                    = "dev"
  aws_availability_zones = ["${data.aws_availability_zones.all.names}"]
  vpc_subnet_tag         = 42
  front_subnet_tag       = 1
  back_subnet_tag        = 2
}
