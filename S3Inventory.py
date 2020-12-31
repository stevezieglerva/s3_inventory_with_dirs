from S3 import *
from collections import namedtuple


AthenaS3Object = namedtuple("AthenaS3Object", "bucket key date size parent1")


class S3Inventory:
    def __init__(self, bucket, s3_injection=S3()):
        self.bucket = bucket
        self.s3 = s3_injection
        pass

    def get_s3_files(self, prefix):
        print(f"get_s3_files: bucket={self.bucket}, prefix={prefix}, s3={S3}")
        files = self.s3.list_objects(self.bucket, prefix, 0)
        return files

    def format_for_athena(self, s3_objects):
        results = []
        for object in s3_objects:
            new_athena = AthenaS3Object(
                bucket=object.bucket,
                key=object.key,
                date=object.date,
                size=object.size,
                parent1="",
            )
            results.append(new_athena)
        return results