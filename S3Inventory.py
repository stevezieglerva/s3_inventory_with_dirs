from S3 import *
from collections import namedtuple


AthenaS3Object = namedtuple(
    "AthenaS3Object",
    "bucket key date size parent1 parent2 parent3 parent4 parent5 parent6 parent7 parent8 parent9 parent10",
)


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
        parent_options = [f"parent{i}" for i in range(1, 11)]
        empty_parent_values = {}
        for parent in parent_options:
            empty_parent_values[parent] = ""

        for object in s3_objects:
            parent_values = empty_parent_values
            folders = object.key.split("/")[:-1]
            for count, folder in enumerate(folders):
                index_number = count + 1
                index = f"parent{index_number}"
                parent_values[index] = folder
            print(parent_values)

            new_athena = AthenaS3Object(
                bucket=object.bucket,
                key=object.key,
                date=object.date,
                size=object.size,
                parent1=parent_values["parent1"],
                parent2=parent_values["parent2"],
                parent3=parent_values["parent3"],
                parent4=parent_values["parent4"],
                parent5=parent_values["parent5"],
                parent6=parent_values["parent6"],
                parent7=parent_values["parent7"],
                parent8=parent_values["parent8"],
                parent9=parent_values["parent9"],
                parent10=parent_values["parent10"],
            )
            results.append(new_athena)
        return results