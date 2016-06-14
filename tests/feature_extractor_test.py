"""Tests for the fex FeatureExtractor."""

import unittest

from fex.feature_extractor import MultipleEmitsError
import mock_extractor as me


class FeatureExtractorTest(unittest.TestCase):
    """Test feature extractor."""

    def test_column_naming(self):
        """Column name should be a combination of class- and col name."""
        test_extractor = me.MockExtractor('1', 'col_1', 42)
        test_extractor.extract()
        col_name = test_extractor.result.columns[0]
        self.assertTrue(col_name.startswith(me.MockExtractor.__name__))
        self.assertTrue(col_name.endswith('col_1'))

    def test_disallow_multiple_emits(self):
        """Should raise an error if we try to emit more than once."""
        test_extractor = me.MockExtractor('1', 'col_1', 42)
        test_extractor.extract()
        # A second extract() call should raise an error
        self.assertRaises(MultipleEmitsError, test_extractor.extract)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
