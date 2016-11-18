output "elb_dns_name" {
  value = "${aws_elb.main.dns_name}"
}

output "version" {
	value = "0.1"
}
