from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)

class EC2CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, userBucket,**kwargs) -> None:
        super().__init__(scope, construct_id ,**kwargs)
        vpc = ec2.Vpc(self, "VPC",
        nat_gateways=0,
        subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
        )

        #userdata
        user_data = ec2.UserData.for_linux()
        user_data.add_commands("sudo su")
        user_data.add_s3_download_command(bucket = userBucket, bucket_key ="script.sh", local_file= "/scripte/")
        #user_data.add_commands("chmod u+x scripte/script.sh")
        user_data.add_commands("scripte/script.sh")
        user_data.add_s3_download_command(bucket = userBucket, bucket_key ="index.html", local_file= "/var/www/html/")
        
        #role 
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        
        #securitygroup
        security_group = ec2.SecurityGroup(
            self,
            "nginx--7623",
            vpc= vpc,
            allow_all_outbound=False)

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80))

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22))
        
        #instance
        ec2.Instance(self, "Instance",
        vpc=vpc,
        instance_type=ec2.InstanceType("t3.nano"),
        machine_image=ec2.AmazonLinuxImage(),
        user_data=user_data,
        allow_all_outbound=True,
        key_name="keypair",
        role = role,
        security_group=security_group)
