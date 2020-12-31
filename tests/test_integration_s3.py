import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import S3


class S3IntegrationTests(unittest.TestCase):
    def test_list_objects__given_valid_bucket__then_list_returned(self):
        # Arrange
        subject = S3()

        # Act

        # Assert


if __name__ == "__main__":
    unittest.main()