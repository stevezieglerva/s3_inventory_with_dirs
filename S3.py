import boto3
from collections import namedtuple
from abc import ABC, abstractmethod

S3Object = namedtuple("S3Object", "bucket key date size")


class S3Base(ABC):
    """Abstract base class for S3 methods allowing local file creation and easier AWS mocking """

    @abstractmethod
    def put_object(self, bucket, key, data):
        raise NotImplementedError

    @abstractmethod
    def list_objects(self, bucket, prefix, total_max=0):
        raise NotImplementedError


class S3(S3Base):
    def put_object(self, bucket, key, data):
        s3 = boto3.client("s3")
        resp = s3.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"key: {key} resp {resp}")
        result = S3Object(bucket=bucket, key=key)
        return result