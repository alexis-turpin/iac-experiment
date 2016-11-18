terraform remote config -backend=s3 ^
 -backend-config="bucket=terraform-states-iac-experiment" ^
 -backend-config="key=dev/web.tfstate" ^
 -backend-config="region=us-east-1" ^
 -backend-config="encrypt=true"
