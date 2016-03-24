"""Tests for the fex FeatureExtractor."""

import os
import tempfile
import unittest

from fex import csv


class CsvTest(unittest.TestCase):
    """Test feature extractor."""

    def setUp(self):
        """Create temporary file and test data."""
        self.test_file = tempfile.mktemp()
        self.test_data = {
            'row_1': {'col1': 1, 'col2': 2},
            'row_2': {'col1': 3},
        }

    def tearDown(self):
        """Remove the directory after the test."""
        os.remove(self.test_file)

    def test_combines_columns_and_add_id(self):
        """The CSV should contain all columns and add an id."""
        csv.dump_dict(self.test_data, self.test_file)
        with open(self.test_file) as f:
            output = f.read().replace('\r', '')
            with open('tests/expected_csv_test_output.csv') as golden_f:
                self.assertEqual(output, golden_f.read())

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
