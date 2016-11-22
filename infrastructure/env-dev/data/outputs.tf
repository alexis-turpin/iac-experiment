output "rds_address" {
  value = "${module.data.rds_address}"
}

output "rds_endpoint" {
  value = "${module.data.rds_endpoint}"
}

output "sg_rds_id" {
  value = "${module.data.sg_rds_id}"
}
