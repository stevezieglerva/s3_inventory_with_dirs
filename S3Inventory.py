from S3 import *
from collections import namedtuple


CSVS3Object = namedtuple(
    "CSVS3Object",
    "bucket key date size parent1 parent2 parent3 parent4 parent5 parent6 parent7 parent8 parent9 parent10",
)

WriteResults = namedtuple("WriteResults", "line_count sample_lines")


class S3Inventory:
    def __init__(self, bucket, s3_injection=S3()):
        self.bucket = bucket
        self.s3 = s3_injection
        pass

    def create_inventory(self, destination_bucket, destination_prefix, source_prefix):
        objects = self.get_s3_files(source_prefix)
        athena_formatted = self.format_for_csv(objects)
        results = self.write_inventory_csv(
            destination_bucket, destination_prefix, athena_formatted
        )
        return results

    def get_s3_files(self, prefix):
        print(f"get_s3_files: bucket={self.bucket}, prefix={prefix}, s3={S3}")
        files = self.s3.list_objects(self.bucket, prefix, 0)
        return files

    def format_for_csv(self, s3_objects):
        results = []
        parent_options = [f"parent{i}" for i in range(1, 11)]

        for object in s3_objects:
            empty_parent_values = {}
            for parent in parent_options:
                empty_parent_values[parent] = ""

            parent_values = empty_parent_values
            folders = object.key.split("/")[:-1]
            for count, folder in enumerate(folders):
                index_number = count + 1
                index = f"parent{index_number}"
                parent_values[index] = folder

            new_athena = CSVS3Object(
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

    def write_inventory_csv(
        self, destination_bucket, destination_prefix, formatted_s3_objects
    ):
        file_text = '"bucket","key","date","size","parent1","parent2","parent3","parent4","parent5","parent6","parent7","parent8","parent9","parent10"\n'
        for object in formatted_s3_objects:
            file_text = (
                file_text
                + f'"{object.bucket}","{object.key}","{object.date}",{object.size},"{object.parent1}","{object.parent2}","{object.parent3}","{object.parent4}","{object.parent5}","{object.parent6}","{object.parent7}","{object.parent8}","{object.parent9}","{object.parent10}"\n'
            )
        self.s3.put_object(
            destination_bucket, f"{destination_prefix}/inventory.csv", file_text
        )
        sample_lines = file_text.split("\n")[0:2]
        results = WriteResults(
            line_count=file_text.count("\n"), sample_lines=sample_lines
        )
        return results
