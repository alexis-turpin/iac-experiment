# Get the data from remote state and amazon
data "terraform_remote_state" "network" {
  backend = "s3"

  config {
    bucket = "terraform-states-iac-experiment"
    key    = "dev/network.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "data" {
  backend = "s3"

  config {
    bucket = "terraform-states-iac-experiment"
    key    = "dev/data.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "${var.region}"
}

module "front" {
  source = "../../modules/web_infra"

  infra                  = "front"
  env                    = "dev"
  min_size               = 2
  max_size               = 5
  instance_port          = 8080
  subnets_id             = ["${data.terraform_remote_state.network.front_subnets}"]
  aws_availability_zones = ["${data.terraform_remote_state.network.network_az}"]
  sg_internal_ssh_id     = "${data.terraform_remote_state.network.sg_internal_ssh_id}"
  vpc_id                 = "${data.terraform_remote_state.network.vpc_id}"

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get upgrade -y
              apt-get install -y python3-pip git
              pip3 install --upgrade pip
              pip3 install pymysql tornado boto3
              cd /tmp
              git clone https://github.com/alexis-turpin/iac-experiment/
              cd iac-experiment/front
              python3 front.py >> front.log
              EOF
}

module "back" {
  source = "../../modules/web_infra"

  infra                  = "back"
  env                    = "dev"
  min_size               = 2
  max_size               = 5
  instance_port          = 8080
  subnets_id             = ["${data.terraform_remote_state.network.back_subnets}"]
  aws_availability_zones = ["${data.terraform_remote_state.network.network_az}"]
  sg_internal_ssh_id     = "${data.terraform_remote_state.network.sg_internal_ssh_id}"
  vpc_id                 = "${data.terraform_remote_state.network.vpc_id}"
  rds_s3_access          = true
  sg_rds_id              = "${data.terraform_remote_state.data.sg_rds_id}"

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get upgrade -y
              apt-get install -y python3-pip git
              pip3 install --upgrade pip
              pip3 install pymysql tornado boto3
              cd /tmp
              git clone https://github.com/alexis-turpin/iac-experiment/
              cd iac-experiment/api
              python3 api.py >> api.log
              EOF
}
