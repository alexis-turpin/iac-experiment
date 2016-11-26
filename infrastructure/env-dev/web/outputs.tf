output "front_elb_dns_name" {
  value = "${module.front.elb_dns_name}"
}

output "back_elb_dns_name" {
  value = "${module.back.elb_dns_name}"
}
