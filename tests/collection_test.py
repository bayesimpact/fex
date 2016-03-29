"""Tests for the fex FeatureExtractor Collection."""

import os
import tempfile
import unittest

import fex
import test_classes as tc


# Python mock library cannot be used because cannot be pickled for caching.
class CallCounterMock(object):
    """Mocking class to count function calls."""

    def __init__(self):
        """Set counter to zero."""
        super(CallCounterMock, self).__init__()
        self.counter = 0

    def __call__(self):
        """Record calls to class instances."""
        self.counter = self.counter + 1


class CollectionTest(unittest.TestCase):
    """Test feature extractor collection."""

    def setUp(self):
        """Create temporary file and test data."""
        self.dataset_file = tempfile.mktemp()
        self.cache_file = tempfile.mktemp()

    def tearDown(self):
        """Remove the file after the test."""
        os.remove(self.dataset_file)
        os.remove(self.cache_file)

    def test_extract_should_not_be_called_if_hash_unchanged(self):
        """Feature extractor should only be re-computed when source changed."""
        test_extractor = tc.TestExtractor('1', 'col_1', 42)
        test_extractor.extract = CallCounterMock()
        collection = fex.Collection(self.cache_file)
        collection.add_feature_extractor(test_extractor)
        collection.run(self.dataset_file)
        self.assertEqual(test_extractor.extract.counter, 1)
        collection = fex.Collection(self.cache_file)
        collection.add_feature_extractor(test_extractor)
        collection.run(self.dataset_file)
        self.assertEqual(test_extractor.extract.counter, 1)
        collection = fex.Collection(self.cache_file)
        collection.add_feature_extractor(test_extractor)
        test_extractor._source_hash = 'new_value'
        collection.run(self.dataset_file)
        self.assertEqual(test_extractor.extract.counter, 2)

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
