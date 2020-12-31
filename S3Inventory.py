from S3 import *


class S3Inventory:
    def __init__(self, bucket, s3_injection=S3()):
        self.bucket = bucket
        self.s3 = s3_injection
        pass

    def get_s3_files(self, prefix):
        print(f"get_s3_files: bucket={self.bucket}, prefix={prefix}, s3={S3}")
        files = self.s3.list_objects(self.bucket, prefix, 0)
        return files