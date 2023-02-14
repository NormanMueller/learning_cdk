from aws_ec2.ec2 import EC2CdkStack
from aws_s3.s3 import S3CdkStack
import aws_cdk as cdk

app = cdk.App()
s3_stack = S3CdkStack(app, "s3-cdk")
EC2CdkStack(app, "ec2-cdk",userBucket=s3_stack.mybucket)
app.synth()
