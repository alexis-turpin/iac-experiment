# Get the data from remote state and amazon
data "terraform_remote_state" "network" {
  backend = "s3"

  config {
    bucket = "terraform-states-iac-experiment"
    key    = "dev/network.tfstate"
    region = "us-east-1"
  }
}

data "aws_availability_zones" "all" {}

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
  subnets_id             = "${data.terraform_remote_state.network.front_subnets}"
  aws_availability_zones = ["${data.aws_availability_zones.all.names}"]
  sg_internal_ssh_id     = "${data.terraform_remote_state.network.sg_internal_ssh_id}"
  vpc_id                 = "${data.terraform_remote_state.network.vpc_id}"

  user_data = <<-EOF
              #!/bin/bash
              echo "I am front :  " > index.html
              curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
              echo "<br>" >> index.html
              curl "http://${module.back.elb_dns_name}" >> index.html
              nohup busybox httpd -f -p 8080 &
              EOF
}

module "back" {
  source = "../../modules/web_infra"

  infra                  = "back"
  env                    = "dev"
  min_size               = 2
  max_size               = 5
  instance_port          = 8080
  subnets_id             = "${data.terraform_remote_state.network.back_subnets}"
  aws_availability_zones = ["${data.aws_availability_zones.all.names}"]
  sg_internal_ssh_id     = "${data.terraform_remote_state.network.sg_internal_ssh_id}"
  vpc_id                 = "${data.terraform_remote_state.network.vpc_id}"

  user_data = <<-EOF
              #!/bin/bash
              echo "I am back :  " > index.html
              curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
              echo "<br>" >> index.html
              nohup busybox httpd -f -p 8080 &
              EOF
}
