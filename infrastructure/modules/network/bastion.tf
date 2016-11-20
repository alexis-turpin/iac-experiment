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

resource "aws_instance" "bastion" {
  instance_type               = "t2.micro"
  ami                         = "${data.aws_ami.ubuntu.image_id}"
  key_name                    = "${var.env}-bastion"
  subnet_id                   = "${aws_subnet.front.0.id}"
  security_groups             = ["${aws_security_group.bastion_ssh.id}"]
  associate_public_ip_address = "True"

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get upgrade -y >> /tmp/done.apt
              cd /tmp
              curl -s https://s3.amazonaws.com/quickstart-reference/linux/bastion/latest/scripts/bastion_bootstrap.sh > bastion_bootstrap.sh
              chmod +x bastion_bootstrap.sh
              /tmp/bastion_bootstrap.sh --enable false >> /tmp/done.bastion
              EOF

  tags {
    Name      = "${var.env}-bastion"
    infra     = "global"
    env       = "${var.env}"
    terraform = "True"
  }
}
