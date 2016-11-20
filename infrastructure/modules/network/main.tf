resource "aws_vpc" "main" {
  cidr_block           = "10.${var.vpc_subnet_tag}.0.0/16"
  enable_dns_hostnames = "True"

  tags {
    Name      = "${var.env}-main-vpc"
    env       = "${var.env}"
    infra     = "global"
    network   = "True"
    terraform = "True"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.main.id}"

  tags {
    Name      = "${var.env}-main-ig"
    env       = "${var.env}"
    infra     = "front"
    network   = "True"
    terraform = "True"
  }
}

resource "aws_subnet" "front" {
  # dirty hard-code for now workaround for issue #1497
  count                   = 4
  availability_zone       = "${element(var.aws_availability_zones, count.index)}"
  vpc_id                  = "${aws_vpc.main.id}"
  cidr_block              = "10.${var.vpc_subnet_tag}.${var.front_subnet_tag}${count.index}.0/24"
  map_public_ip_on_launch = "True"

  tags {
    Name      = "${var.env}-front-${element(var.aws_availability_zones, count.index)}"
    env       = "${var.env}"
    infra     = "front"
    network   = "True"
    terraform = "True"
  }
}

resource "aws_subnet" "back" {
  # dirty hard-code for now workaround for issue 1497
  count                   = 4
  availability_zone       = "${element(var.aws_availability_zones, count.index)}"
  vpc_id                  = "${aws_vpc.main.id}"
  cidr_block              = "10.${var.vpc_subnet_tag}.${var.back_subnet_tag}${count.index}.0/24"
  map_public_ip_on_launch = "True"

  tags {
    Name      = "${var.env}-back-${element(var.aws_availability_zones, count.index)}"
    env       = "${var.env}"
    infra     = "back"
    network   = "True"
    terraform = "True"
  }
}

resource "aws_route" "vpc_to_wan" {
  route_table_id         = "${aws_vpc.main.default_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.main.id}"
}
