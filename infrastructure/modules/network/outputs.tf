output "front_subnets" {
  value = ["${aws_subnet.front.*.id}"]
}
output "back_subnets" {
  value = ["${aws_subnet.back.*.id}"]
}

output "sg_internal_ssh_id" {
  value = "${aws_security_group.internal_ssh.id}"
}

output "vpc_id" {
  value = "${aws_vpc.main.id}"
}

output "version" {
	value = "0.1"
}
