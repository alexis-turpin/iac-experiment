## Web_infra

This module is creating one [AutoScaling Group (ASG)](https://aws.amazon.com/autoscaling/) and its launch configuration.
All created instances will be automatically linked to the module's 
[Elastic Load Balancer (ELB)](https://aws.amazon.com/elasticloadbalancing/).

### Variables
  - `infra`: Infrastructure to deploy. (Used for naming / tagging)
  - `env`: Environment to deploy. (Used for naming /tagging)
  - `user_data`: Script to execute on the launched instances
  - `key_name`: SSH key to link to launched instances
  - `min_size`: Minimum size of the ASG (in number of instances)
  - `max_size`: Maximum size of the ASG (in number of instances)
  - `instance_type`: Type of instance to launch (t2.micro is free tier)
  - `instance_port`: Port on which instances will listen to HTTP traffic
  - `open_port`: Outgoing port to open on instances (to download their configuration, update packages...) - `list`
  - `elb_port`: Port on which the ELB will listen to http request
  - `subnet_id`: List of subnets to be used by instances - `list`
  - `vpc_id`: Environment dedicated VPC. Used to created security groups
  - `sg_internal_ssh_id`: ID of the security group allow ssh connections between bastion and instance"
  - `aws_availability_zones`: List of available AZ in my region - `list`
  - `rds_access`: Access to the database - `bool`
  - `sg_rds_id`: Security group allowing access to the db

### Outputs
  - `elb_dns_name`: DNS name of the ELB, the name to use to access instances created by this module.
