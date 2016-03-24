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

    def test_combines_columns(self):
        """The CSV should contain all columns."""
        csv.dump_dict(self.test_data, self.test_file)
        with (open(self.test_file)) as f:
            out = f.readlines()
            header = out[0].strip()
            col_names = header.split(',')[1:]
            self.assertEqual(set(col_names), set(['col1', 'col2']))

    def test_id_column_added(self):
        """The CSV should start with an id column."""
        csv.dump_dict(self.test_data, self.test_file)
        with (open(self.test_file)) as f:
            out = f.readlines()
            header = out[0].strip()
            self.assertTrue(header.startswith('id'))

    def test_ids_correctly_set(self):
        """The CSV should have the id values correctly set."""
        csv.dump_dict(self.test_data, self.test_file)
        with (open(self.test_file)) as f:
            out = f.readlines()
            data_rows = out[1:]
            id_vals = [row.split(',')[0] for row in data_rows]
            self.assertEqual(set(id_vals), set(['row_1', 'row_2']))

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
