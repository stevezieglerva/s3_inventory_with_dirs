import unittest
from unittest import mock
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import *
from S3Inventory import S3Inventory, AthenaS3Object


class S3InventoryUnitTests(unittest.TestCase):
    def test_get_s3_files__given_valid_prefix__then_correct_formatted_returned(self):
        # Arrange
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        with mock.patch(
            "S3.S3FakeLocal.list_objects",
            mock.MagicMock(return_value=["faked"]),
        ):
            results = subject.get_s3_files("failed")

        # Assert
        self.assertGreater(len(results), 0)

    def test_format_for_athena__given_one_file__then_results_formatted_correctly(
        self,
    ):
        # Arrange
        input = [
            S3Object(
                bucket="fake-bucket", key="dir1/object_1", date="2020-01-01", size=100
            )
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.format_for_athena(input)

        # Assert
        self.assertGreater(len(results), 0)
        expected = AthenaS3Object(
            bucket=input[0].bucket,
            key=input[0].key,
            date=input[0].date,
            size=input[0].size,
            parent1="dir1",
            parent2="",
            parent3="",
            parent4="",
            parent5="",
            parent6="",
            parent7="",
            parent8="",
            parent9="",
            parent10="",
        )
        print(results[0])
        print(expected)
        self.assertEqual(results[0], expected)

    def test_format_for_athena__given_one_file_with_10_folders__then_results_formatted_correctly(
        self,
    ):
        # Arrange
        input = [
            S3Object(
                bucket="fake-bucket",
                key="a/b/c/d/e/f/g/h/i/j/object_1",
                date="2020-01-01",
                size=100,
            )
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.format_for_athena(input)

        # Assert
        self.assertGreater(len(results), 0)
        expected = AthenaS3Object(
            bucket=input[0].bucket,
            key=input[0].key,
            date=input[0].date,
            size=input[0].size,
            parent1="a",
            parent2="b",
            parent3="c",
            parent4="d",
            parent5="e",
            parent6="f",
            parent7="g",
            parent8="h",
            parent9="i",
            parent10="j",
        )
        print(results[0])
        print(expected)
        self.assertEqual(results[0], expected)

    def test_write_inventory__given_formatted_results__then_correct_count_returned(
        self,
    ):
        # Arrange
        input = [
            AthenaS3Object(
                bucket="bucket-1",
                key="dir1/dir2/file.txt",
                date="2020-01-01",
                size=100,
                parent1="dir1",
                parent2="dir2",
                parent3="",
                parent4="",
                parent5="",
                parent6="",
                parent7="",
                parent8="",
                parent9="",
                parent10="",
            )
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.write_inventory_csv(
            "inventory-results-bucket", "pictures", input
        )

        # Assert
        self.assertEqual(results, 2)


if __name__ == "__main__":
    unittest.main()