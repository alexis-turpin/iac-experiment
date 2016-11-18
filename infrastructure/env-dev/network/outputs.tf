output "front_subnets" {
  value = "${module.network.front_subnets}"
}

output "back_subnets" {
  value = "${module.network.back_subnets}"
}

output "sg_internal_ssh_id" {
  value = "${module.network.sg_internal_ssh_id}"
}

output "vpc_id" {
  value = "${module.network.vpc_id}"
}

output "network_version" {
  value = "${module.network.version}"
}
