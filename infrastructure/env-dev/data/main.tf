data "terraform_remote_state" "network" {
  backend = "s3"

  config {
    bucket = "terraform-states-iac-experiment"
    key    = "dev/network.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "${var.region}"
}

module "data" {
  source = "../../modules/data"

  env         = "dev"
  subnets_id  = ["${data.terraform_remote_state.network.back_subnets}"]
  cidr_blocks = ["${data.terraform_remote_state.network.back_subnets_cidr}"]
  vpc_id      = "${data.terraform_remote_state.network.vpc_id}"
}
