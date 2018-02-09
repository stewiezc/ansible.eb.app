# ansible.eb.app
ansible playbook to build elastic beanstalk app and environment

Requirements
------------
- terraform on path
- terragrunt on path

How to use
----------
This should be run against localhost. You have to set a var to true for the action you want terragrunt to perform. 

`ansible-playbook -i localhost, -c local playbook.yml -e "env=QA" -e "plan=true"`

- `plan=true` - terragrunt plan
- `apply=true` - terragrunt apply
- `plan=true, destroy=true` - terragrunt plan -destroy
- `destroy=true` - terragrunt destroy -force !!dangerous

Example playbook

```
- hosts: all
  vars_files:
    - vars.yml
    - secrets.yml
  pre_tasks:
    - include_vars: "{{ item }}"
      with_first_found:
        - vars_{{ env }}.yml
        - vars.yml
  roles:
    - dms-ansible-eb-app
```

Variables
---------
Required
- `name` - Application Name
- `env` - Prod/Non-Prod/QA/Dev
- `aws_account` - Name of AWS account - example awsacctabc
- `notification_email` - Email address to receive notifications

Optional
- `aws_region` - region to deploy to - Default = us-east-1
- `terragrunt_s3_bucket` - bucket to store state files - Default = aws_account.terragrunt
- `terragrunt_state_file_id` - dynamodb lock location - Default = name
- `terragrunt_s3_region` - Default = us-east-1
- `terragrunt_app_s3_key` - state file location for elastic beanstalk app - Default = name/terraform.tfstate
- `terragrunt_env_s3_key` - state file location for elastic beanstalk environment - Default = name-env/terraform.tfstate
- `stack` - The application stack - http://docs.aws.amazon.com/fr_fr/elasticbeanstalk/latest/dg/concepts.platforms.html - Default = 64bit Amazon Linux 2016.03 v2.1.6 running Docker 1.11.2
- `healthcheck_url` - The URL to perform health checks - Default = /health
- `ec2keyname` - Keypair to log into EC2 instances
- `crosszone` - load balance accross availability zones - Default = true
- `autoscaling_minsize` - Minimum number of instances - Default = 1
- `autoscaling_maxsize` - Maximum number of instances - Default = 2
- `deployment_policy` - AllAtOnce, Rolling, Immutable - Default = Rolling
- `instance_type` - Platform and stack dependant - Default = t2.micro
- `connection_draining_enabled` - Maintain existing requests to unhealthy instances - Default = false
- `connection_draining_timeout` - number of seconds to maintain connections - Default = 20
- `rolling_update_enabled` - enable rolling updates - Default = true
- `rolling_update_type` - Time, Health, or Immutable - Default = Health
- `service_role` - IAM role required for enhanced logging and managed updates - Default = aws-elasticbeanstalk-service-role
- `system_type` - Health Reporting type basic/enhanced - Default = enhanced
- `managed_actions_enabled` - Enabled managed patching - Default = true
- `preferred_start_time` - Time to start patching in UTC - Default = Tue:05:00
- `update_level` - What patch level major/minor/patch - Default = patch
- `iam_instance_profile` - Allows an instance to get security credentials - Default = aws-elasticbeanstalk-ec2-role

VPC - If vpc_id is not specified these settings won't be rendered at all
- `vpc_id` - ID for VPC to use
- `subnet_tag_name` - Tag to search for - example "tags.SUB-Type"
- `subnet_tag_autoscaling` - Value of subnet_tag_name to discover autoscaling subnets - Default = Public
- `subnet_tag_elb` - Value of subnet_tag_name to discover elb subnets - Default = Public
- `autoscaling_subnets` - subnets in autoscaling group - These will be auto defined if the above are specified - define as [list,] if manual
- `elb_subnets` - subnets for the load balancer - These will be auto defined if the above are specified - define as list [list,] if manual
- `associate_public_ip_address` - specify whether to launch instances with a public IP
- `elb_scheme` - specify `internal` if you want to create an internal load balancer 

ELB Listener - http and/or https on your elb - http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html#command-options-general-elblistener

Define an elb_listeners variable - default is to disable http and only have https with dtdms.io wildcard cert attached.

```
cert_discover: True
cert_name: "*.dtdms.io"
elb_listeners:
  - listener_port: 443
    listener_protocol: HTTPS
    listener_enabled: "true"
    instance_port: 80
    instance_protocol: HTTP
    ssl_certificate_id: {{ cert_arn }}
  - listener_port: 80
    listener_protocol: HTTP
    listener_enabled: "false"
    instance_port: 80
    instance_protocol: HTTP
    ssl_certificate_id: "None"
```

 
You can also create a var named platform_specific and render any additional settings you want

```
platform_specific:
  - namespace: aws:namespace
    name: Config
    value: "true"
  - namespace: aws:anothernamespace
    name: MoreConfig
    value: "false"
```