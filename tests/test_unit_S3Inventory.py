import unittest
from unittest import mock
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from S3 import *
from S3Inventory import S3Inventory, CSVS3Object, WriteResults
from datetime import datetime


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

    def test_format_for_csv__given_one_file__then_results_formatted_correctly(
        self,
    ):
        # Arrange
        input = [
            S3Object(
                bucket="fake-bucket",
                key="dir1/object_1",
                date=datetime(2020, 7, 15),
                size=100,
            )
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.format_for_csv(input)

        # Assert
        self.assertGreater(len(results), 0)
        expected = CSVS3Object(
            bucket=input[0].bucket,
            key=input[0].key,
            timestamp=input[0].date,
            date="2020-07-15",
            year=2020,
            month=7,
            day=15,
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
        self.assertEqual(results[0], expected)

    def test_format_for_csv__given_one_file_with_10_folders__then_results_formatted_correctly(
        self,
    ):
        # Arrange
        input = [
            S3Object(
                bucket="fake-bucket",
                key="a/b/c/d/e/f/g/h/i/j/object_1",
                date=datetime(2020, 7, 15),
                size=100,
            )
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.format_for_csv(input)

        # Assert
        self.assertGreater(len(results), 0)
        expected = CSVS3Object(
            bucket=input[0].bucket,
            key=input[0].key,
            timestamp=input[0].date,
            date="2020-07-15",
            year=2020,
            month=7,
            day=15,
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
        self.assertEqual(results[0], expected)

    def test_write_inventory__given_two_parents__then_correct_count_returned(
        self,
    ):
        # Arrange
        input = [
            CSVS3Object(
                bucket="bucket-1",
                key="dir1/dir2/two_parents.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
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
        expected = WriteResults(
            line_count=2,
            sample_lines=[
                '"bucket","key","timestamp","date","year","month","day","size","parent1","parent2","parent3","parent4","parent5","parent6","parent7","parent8","parent9","parent10"',
                '"bucket-1","dir1/dir2/two_parents.txt","2020-01-01T00:00:00","2020-01-01","2020","1","1",100,"dir1","dir2","","","","","","","",""',
            ],
        )
        print("\n\n")
        print(results)
        print(expected)
        self.assertEqual(results, expected)

    def test_write_inventory__given_ten_parents__then_correct_count_returned(
        self,
    ):
        # Arrange
        input = [
            CSVS3Object(
                bucket="bucket-1",
                key="dir1/dir2/ten_parents.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
                size=100,
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
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.write_inventory_csv(
            "inventory-results-bucket", "pictures", input
        )

        # Assert
        expected = WriteResults(
            line_count=2,
            sample_lines=[
                '"bucket","key","timestamp","date","year","month","day","size","parent1","parent2","parent3","parent4","parent5","parent6","parent7","parent8","parent9","parent10"',
                '"bucket-1","dir1/dir2/ten_parents.txt","2020-01-01T00:00:00","2020-01-01","2020","1","1",100,"a","b","c","d","e","f","g","h","i","j"',
            ],
        )
        print("\n\n")
        print(results)
        print(expected)
        self.assertEqual(results, expected)

    def test_write_inventory__given_several_rows__then_correct_count_returned(
        self,
    ):
        # Arrange
        input = [
            CSVS3Object(
                bucket="bucket-1",
                key="a/b/c/d/e/f/g/h/i/j/file.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
                size=100,
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
            ),
            CSVS3Object(
                bucket="bucket-1",
                key="a/b/file.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
                size=100,
                parent1="a",
                parent2="b",
                parent3="",
                parent4="",
                parent5="",
                parent6="",
                parent7="",
                parent8="",
                parent9="",
                parent10="",
            ),
            CSVS3Object(
                bucket="bucket-1",
                key="a/file.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
                size=100,
                parent1="a",
                parent2="",
                parent3="",
                parent4="",
                parent5="",
                parent6="",
                parent7="",
                parent8="",
                parent9="",
                parent10="",
            ),
            CSVS3Object(
                bucket="bucket-1",
                key="a/b/file2.txt",
                timestamp="2020-01-01T00:00:00",
                date="2020-01-01",
                year=2020,
                month=1,
                day=1,
                size=100,
                parent1="a",
                parent2="b",
                parent3="",
                parent4="",
                parent5="",
                parent6="",
                parent7="",
                parent8="",
                parent9="",
                parent10="",
            ),
        ]
        subject = S3Inventory("fake-bucket", S3FakeLocal())

        # Act
        results = subject.write_inventory_csv(
            "inventory-results-bucket", "pictures", input
        )

        # Assert
        expected = WriteResults(
            line_count=5,
            sample_lines=[
                '"bucket","key","timestamp","date","year","month","day","size","parent1","parent2","parent3","parent4","parent5","parent6","parent7","parent8","parent9","parent10"',
                '"bucket-1","a/b/c/d/e/f/g/h/i/j/file.txt","2020-01-01T00:00:00","2020-01-01","2020","1","1",100,"a","b","c","d","e","f","g","h","i","j"',
            ],
        )
        self.assertEqual(results, expected)


if __name__ == "__main__":
    unittest.main()