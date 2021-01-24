import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import *
from S3Inventory import S3Inventory


class S3InventoryIntegrationTests(unittest.TestCase):
    def test_get_s3_files__given_valid_prefix__then_correct_formatted_returned(self):
        # Arrange
        subject = S3Inventory("svz-master-pictures-new", S3())

        # Act
        results = subject.get_s3_files("failed")

        # Assert
        self.assertGreater(len(results), 0)

    def test_create_inventory__given_valid_bucket__then_file_created(self):
        # Arrange
        subject = S3Inventory("svz-master-pictures-new", S3())

        # Act
        results = subject.create_inventory(
            "svz-master-pictures-new", "inventory", "failed"
        )

        # Assert
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()