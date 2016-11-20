# Data queries
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Instance configuration
resource "aws_autoscaling_group" "instance" {
  name                 = "${var.env}-${var.infra}-asg"
  launch_configuration = "${aws_launch_configuration.instance.id}"
  availability_zones   = ["${var.aws_availability_zones}"]
  load_balancers       = ["${aws_elb.main.name}"]
  vpc_zone_identifier  = ["${var.subnets_id}"]
  health_check_type    = "ELB"

  # 5 minutes before starting to check health, could be reduced
  health_check_grace_period = 300
  min_size                  = "${var.min_size}"
  max_size                  = "${var.max_size}"
  termination_policies      = ["OldestInstance"]

  tag {
    key                 = "Name"
    value               = "${var.env}-${var.infra}-server"
    propagate_at_launch = true
  }

  tag {
    key                 = "infra"
    value               = "${var.infra}"
    propagate_at_launch = true
  }

  tag {
    key                 = "env"
    value               = "${var.env}"
    propagate_at_launch = true
  }

  tag {
    key                 = "terraform"
    value               = "True"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "instance" {
  name_prefix     = "${var.env}-${var.infra}-conf"
  image_id        = "${data.aws_ami.ubuntu.image_id}"
  instance_type   = "${var.instance_type}"
  security_groups = ["${aws_security_group.instance.id}", "${var.sg_internal_ssh_id}"]
  user_data       = "${var.user_data}"
  key_name        = "${var.key_name}"
}

#  Load-balancer
resource "aws_elb" "main" {
  name            = "${var.env}-${var.infra}-elb"
  security_groups = ["${aws_security_group.main_elb.id}"]
  subnets         = ["${var.subnets_id}"]

  listener {
    lb_port           = "${var.elb_port}"
    lb_protocol       = "http"
    instance_port     = "${var.instance_port}"
    instance_protocol = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 10
    target              = "HTTP:${var.instance_port}/"
  }

  tags {
    Name      = "${var.env}-${var.infra}-elb"
    infra     = "${var.infra}"
    env       = "${var.env}"
    terraform = "True"
  }
}
