import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import json
import os, sys, inspect
from collections import namedtuple


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/export_jira_data"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

from export_jira_data import app


class S3FakeLocal(app.S3Base):
    def put_object(self, bucket, key, data):
        key = key.replace("/", "__")
        filename = f"test_fakes3_integration_{bucket}__{key}"
        with open(filename, "w") as file:
            file.write(data)
        result = app.S3Object(bucket="local", key=filename)
        return result


class ExportJiraDataIntegrationTests(unittest.TestCase):
    def test_lambda_handler__given_jira_data_found__then_counts_are_positive(self):
        # Arrange
        os.environ["TOTAL"] = "0"
        os.environ["BATCH_LIMIT"] = "500"
        os.environ["S3_BUCKET"] = "fake-bucket"
        s3_object = S3FakeLocal()

        # Act
        results = app.main("", "", s3_object)

        # Assert
        self.assertGreater(results["issue_count"], 10)

    def test_lambda_handler__given_total_and_batch_limits__then_counts_are_correct(
        self,
    ):
        # Arrange
        os.environ["TOTAL"] = "4"
        os.environ["BATCH_LIMIT"] = "2"
        os.environ["S3_BUCKET"] = "fake-bucket"
        s3_object = S3FakeLocal()

        # Act
        results = app.main("", "", s3_object)

        # Assert
        self.assertEqual(results["issue_count"], 4)
        self.assertEqual(len(results["issues"]), 4)
        print("\n\n************\n")
        print(results["issues"])


if __name__ == "__main__":
    unittest.main()