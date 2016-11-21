resource "aws_security_group" "rds_sg" {
  name        = "${var.env}-db"
  description = "Allow connection from back subnets on 3306"

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "TCP"
    cidr_blocks = ["${var.cidr_blocks}"]
  }

  vpc_id = "${var.vpc_id}"

  tags {
    Name      = "${var.env}-data-sg"
    env       = "${var.env}"
    infra     = "data"
    terraform = true
  }
}
