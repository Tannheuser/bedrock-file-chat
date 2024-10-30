import boto3
from operator import itemgetter


class AwsService:
    def __init__(self, aws_profile=None):
        self.__aws_profile = aws_profile

        if aws_profile:
            self.__session = boto3.Session(profile_name=aws_profile)
        else:
            self.__session = boto3.Session()

        self.__s3_client = self.__session.client("s3")
        self.__bedrock_client = self.__session.client("bedrock-agent-runtime")

    def _get_model_configuration(self, model_id, s3_url=None, file=None):
        model_arn = (
            f"arn:aws:bedrock:{self.__session.region_name}::foundation-model/{model_id}"
        )
        source = (
            {"sourceType": "S3", "s3Location": {"uri": s3_url}}
            if s3_url
            else {
                "sourceType": "BYTE_CONTENT",
                "byteContent": {
                    "contentType": "application/pdf",
                    "data": file.read(),
                    "identifier": file.name,
                },
            }
        )
        return {
            "type": "EXTERNAL_SOURCES",
            "externalSourcesConfiguration": {
                "modelArn": model_arn,
                "sources": [source],
            },
        }

    def list_files(self, bucket_name):
        response = self.__s3_client.list_objects(Bucket=bucket_name)
        return response["Contents"]

    def get_llm_response(self, params):
        query = params.get("query")
        model_id = params.get("model_id")
        bucket_name = params.get("bucket_name")
        file_name = params.get("file_name")
        file = params.get("file")

        if file is not None:
            config = self._get_model_configuration(model_id, file=file)
        else:
            s3_url = f"s3://{bucket_name}/{file_name}"
            config = self._get_model_configuration(model_id, s3_url)

        response = self.__bedrock_client.retrieve_and_generate(
            input={"text": query}, retrieveAndGenerateConfiguration=config
        )
        return response["output"]["text"]
