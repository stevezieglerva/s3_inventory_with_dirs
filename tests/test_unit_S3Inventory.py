import unittest
from unittest import mock
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import *
from S3Inventory import S3Inventory


class S3InventoryUnitTests(unittest.TestCase):
    def test_get_s3_files__given_valid_prefix__then_correct_formatted_returned(self):
        # Arrange
        subject = S3Inventory("fake-bucket", S3FakeLocal)

        # Act
        with mock.patch(
            "S3.S3FakeLocal.list_objects",
            mock.MagicMock(return_value=["faked"]),
        ):
            results = subject.get_s3_files("failed")

        # Assert
        self.assertGreater(len(results), 0)

    def test_format_for_athena__given_some_files__then_results_formatted_correctly(
        self,
    ):
        # Arrange
        input = [
            S3Object(bucket="fake-bucket", key="object_1", date="2020-01-01", size=100)
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal)

        # Act
        results = subject.format_for_athena(input)

        # Assert
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()