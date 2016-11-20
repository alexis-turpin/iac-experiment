resource "aws_security_group" "internal_ssh" {
  name        = "${var.env}-internal-ssh"
  description = "Allow all internal SSH 22 traffic in our current VPC"
  vpc_id      = "${aws_vpc.main.id}"

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = ["${aws_security_group.bastion_ssh.id}"]
  }

  tags {
    env       = "${var.env}"
    infra     = "global"
    terraform = "True"
  }
}

resource "aws_security_group" "bastion_ssh" {
  name        = "${var.env}-bastion-ssh"
  description = "Allow incomming SSH traffic from all and allow outgoing SSH to internal instances"
  vpc_id      = "${aws_vpc.main.id}"

  tags {
    env       = "${var.env}"
    infra     = "global"
    terraform = "True"
  }
}

resource "aws_security_group_rule" "bastion_from_wan_ssh" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = "${aws_security_group.bastion_ssh.id}"
}

resource "aws_security_group_rule" "bastion_to_instance_ssh" {
  type        = "egress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["${aws_vpc.main.cidr_block}"]

  security_group_id = "${aws_security_group.bastion_ssh.id}"
}

resource "aws_security_group_rule" "bastion_to_wan" {
  count       = "${length(var.bastion_open_ports)}"
  type        = "egress"
  from_port   = "${element(var.bastion_open_ports, count.index)}"
  to_port     = "${element(var.bastion_open_ports, count.index)}"
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = "${aws_security_group.bastion_ssh.id}"
}
