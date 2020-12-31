import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import S3


class S3IntegrationTests(unittest.TestCase):
    def test_list_objects__given_valid_bucket_10_max__then_list_returned(self):
        # Arrange
        subject = S3()

        # Act
        results = subject.list_objects("svz-master-pictures-new", "failed", 10)

        # Assert
        self.assertEqual(len(results), 10)
        print(results[0])

    def test_list_objects__given_valid_bucket_no_max__then_list_returned(self):
        # Arrange
        subject = S3()

        # Act
        results = subject.list_objects("svz-master-pictures-new", "failed")

        # Assert
        self.assertGreater(len(results), 10)
        print(results[0])


if __name__ == "__main__":
    unittest.main()