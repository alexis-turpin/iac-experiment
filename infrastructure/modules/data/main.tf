resource "aws_db_instance" "main" {
  allocated_storage      = "${var.allocated_storage}"
  instance_class         = "${var.instance_class}"
  engine                 = "mysql"
  identifier             = "${var.env}-banana"
  storage_type           = "gp2"
  name                   = "${var.env}banana"
  password               = "${var.db_password}"
  username               = "root"
  multi_az               = false
  publicly_accessible    = false
  db_subnet_group_name   = "${aws_db_subnet_group.back.id}"
  vpc_security_group_ids = ["${aws_security_group.rds_sg.id}"]

  tags {
    Name      = "${var.env}-banana"
    env       = "${var.env}"
    infra     = "data"
    terraform = true
  }
}

resource "aws_db_subnet_group" "back" {
  name        = "${var.env}-db-subnet"
  description = "${var.env} - Banana DB to back"
  subnet_ids  = ["${var.subnets_id}"]

  tags {
    Name      = "${var.env}-banana"
    env       = "${var.env}"
    infra     = "data"
    terraform = true
  }
}
