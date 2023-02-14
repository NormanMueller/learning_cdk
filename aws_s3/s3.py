from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3,
    aws_s3_deployment as s3deploy,
)

class S3CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket = aws_s3.Bucket(self, "bkasdasdjd22os",block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL)
        
        deployment_index = s3deploy.BucketDeployment(
                scope = self, 
                id = "index",
                sources=[s3deploy.Source.asset("website")], 
                destination_bucket= bucket)
        
        self.mybucket =bucket
