import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import *
from S3Inventory import S3Inventory


class S3InventoryUnitTests(unittest.TestCase):
    def test_get_s3_files__given_valid_prefix__then_correct_formatted_returned(self):
        # Arrange
        subject = S3Inventory("fake-bucket", S3FakeLocal)
        print(subject.bucket)

        # Act
        results = subject.get_s3_files("failed")

        # Assert
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()