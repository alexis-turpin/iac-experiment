output "rds_address" {
  value = "${aws_db_instance.main.address}"
}

output "rds_endpoint" {
  value = "${aws_db_instance.main.endpoint}"
}

output "sg_rds_id" {
  value = "${aws_security_group.rds_sg.id}"
}
