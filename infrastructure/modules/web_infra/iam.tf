# If we should have access to S3
resource "aws_iam_role" "s3_access" {
  count = "${var.rds_s3_access}"
  name  = "${var.env}-${var.infra}-S3_access"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "s3_access_role_policy" {
  count = "${var.rds_s3_access}"
  name  = "s3_access_role_policy"
  role  = "${aws_iam_role.s3_access.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Resource": "arn:aws:s3:::terraform-states-iac-experiment/${var.env}/*"
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "S3_true" {
  count = "${var.rds_s3_access}"
  name  = "${var.env}-${var.infra}-profile"
  roles = ["${var.env}-${var.infra}-S3_access"]
}

#Else empty iam instance profile
resource "aws_iam_instance_profile" "S3_false" {
  count = "${1 - var.rds_s3_access}"
  name  = "${var.env}-${var.infra}-profile"
  roles = ["${var.env}-${var.infra}-empty"]
}

resource "aws_iam_role" "empty_role" {
  count = "${1 - var.rds_s3_access}"
  name  = "${var.env}-${var.infra}-empty"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
