"""Tests for the fex FeatureExtractor."""

import unittest
import test_classes as tc


class FeatureExtractorTest(unittest.TestCase):
    """Test feature extractor."""

    def test_column_naming(self):
        """Column name should be a combination of class- and col name."""
        test_extractor = tc.TestExtractor('1', 'col_1', 42)
        test_extractor.extract()
        row = test_extractor._data_store['1']
        col_name = list(row.keys())[0]
        self.assertTrue(col_name.startswith(tc.TestExtractor.__name__))
        self.assertTrue(col_name.endswith('col_1'))

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
