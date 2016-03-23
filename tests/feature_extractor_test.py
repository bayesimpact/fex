"""Tests for the fex FeatureExtractor."""

import unittest

from fex import FeatureExtractor


class TestExtractor(FeatureExtractor):
    """A very simple test extractor."""

    def __init__(self, row_id, col_name, value):
        """Remember values to make tests more readable."""
        super(TestExtractor, self).__init__()
        self.row_id = row_id
        self.col_name = col_name
        self.value = value

    def extract(self):
        """Overriden method to emit data."""
        self.emit(self.row_id, self.col_name, self.value)


class FeatureExtractorTest(unittest.TestCase):
    """Test feature extractor."""

    def test_column_naming(self):
        """Column name should be a combination of class- and col name."""
        test_extractor = TestExtractor('1', 'col_1', 42)
        test_extractor.extract()
        row = test_extractor._data_store['1']
        col_name = list(row.keys())[0]
        self.assertTrue(col_name.startswith(TestExtractor.__name__))
        self.assertTrue(col_name.endswith('col_1'))

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
