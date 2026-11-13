
import boto3
from botocore.stub import Stubber

from s3_checker import object_exists


def test_existing_object_returns_true():
    s3 = boto3.client(
        "s3",
        region_name="eu-north-1",
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
    )
    bucket = "lesson-25-bucket"
    key = "models/model.pkl"

    with Stubber(s3) as stub:
        stub.add_response(
            "head_object",
            {"ContentLength": 1024},
            expected_params={"Bucket": bucket, "Key": key},
        )

        assert object_exists(s3, bucket, key) is True
        stub.assert_no_pending_responses()

def test_missing_object_returns_false():
    s3 = boto3.client(
        "s3",
        region_name="eu-north-1",
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
    )
    bucket = "lesson-25-bucket"
    key = "models/missing-model.pkl"

    with Stubber(s3) as stub:
        stub.add_client_error(
            "head_object",
            service_error_code="404",
            service_message="Not Found",
            http_status_code=404,
            expected_params={"Bucket": bucket, "Key": key},
        )

        result = object_exists(s3, bucket, key)
        assert result is False
        stub.assert_no_pending_responses()