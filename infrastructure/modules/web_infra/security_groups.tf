# Security_groups
resource "aws_security_group" "instance" {
  name_prefix = "${var.env}-${var.infra}-"
  description = "${var.env}-${var.infra} - Allow all communication from ELB to choosen port"
  vpc_id      = "${var.vpc_id}"

  tags {
    Name      = "${var.env}-${var.infra}-sg"
    infra     = "${var.infra}"
    env       = "${var.env}"
    terraform = "True"
  }
}

resource "aws_security_group_rule" "instance_from_elb" {
  type                     = "ingress"
  source_security_group_id = "${aws_security_group.main_elb.id}"
  from_port                = "${var.instance_port}"
  to_port                  = "${var.instance_port}"
  protocol                 = "tcp"
  security_group_id        = "${aws_security_group.instance.id}"
}

resource "aws_security_group_rule" "instance_to_wan" {
  count             = "${length(var.open_port)}"
  type              = "egress"
  from_port         = "${element(var.open_port, count.index)}"
  to_port           = "${element(var.open_port, count.index)}"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.instance.id}"
}

resource "aws_security_group" "main_elb" {
  name_prefix = "${var.env}-${var.infra}-ELB-"
  description = "${var.env}-${var.infra} - Allow communication from WAN to ELB (port ${var.elb_port}) and from ELB to instances (port ${var.elb_port})"
  vpc_id      = "${var.vpc_id}"

  tags {
    Name      = "${var.env}-${var.infra}-ELB"
    infra     = "${var.infra}"
    env       = "${var.env}"
    terraform = "True"
  }
}

resource "aws_security_group_rule" "elb_to_instance" {
  type                     = "egress"
  from_port                = "${var.instance_port}"
  to_port                  = "${var.instance_port}"
  protocol                 = "tcp"
  source_security_group_id = "${aws_security_group.instance.id}"
  security_group_id        = "${aws_security_group.main_elb.id}"
}

resource "aws_security_group_rule" "elb_from_wan" {
  type              = "ingress"
  from_port         = "${var.elb_port}"
  to_port           = "${var.elb_port}"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.main_elb.id}"
}
