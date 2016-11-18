resource "aws_security_group" "internal_ssh" {
  name_prefix = "internal_ssh"
  description = "Allow all internal SSH 22 traffic in our current VPC"
  vpc_id = "${aws_vpc.main.id}"
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    self = true
  }
  egress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    self = true
  }
  tags {
    Name = "${var.env}-internal-ssh"
    env = "${var.env}"
    infra = "global"
    terraform = "True"
  }
}
