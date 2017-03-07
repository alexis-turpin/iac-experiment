output "front_subnets" {
  value = ["${aws_subnet.front.*.id}"]
}

output "back_subnets" {
  value = ["${aws_subnet.back.*.id}"]
}

output "back_subnets_cidr" {
  value = ["${aws_subnet.back.*.cidr_block}"]
}

output "sg_internal_ssh_id" {
  value = "${aws_security_group.internal_ssh.id}"
}

output "vpc_id" {
  value = "${aws_vpc.main.id}"
}

output "bastion_ip" {
  value = "${aws_instance.bastion.public_ip}"
}

output "network_az" {
  value = "${var.aws_availability_zones}"
}
