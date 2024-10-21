import boto3


class AwsService:
    def __init__(self, aws_profile=None):
        self.__aws_profile = aws_profile

        if aws_profile:
            self.__session = boto3.Session(profile_name=aws_profile)
        else:
            self.__session = boto3.Session()

        self.__s3_client = self.__session.client("s3")
        self.__bedrock_client = self.__session.client("bedrock-agent-runtime")

    def list_files(self, bucket_name):
        response = self.__s3_client.list_objects(Bucket=bucket_name)
        return response["Contents"]
