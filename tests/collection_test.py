"""Tests for the fex FeatureExtractor Collection."""

import os
import tempfile
import unittest

import fex
import mock_extractor as me


# Python mock library cannot be used because cannot be pickled for caching.
class _CallCounterMock(object):
    """Mocking class to count function calls."""

    def __init__(self):
        """Set counter to zero."""
        super(_CallCounterMock, self).__init__()
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
        for f in [self.dataset_file, self.cache_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_extract_should_not_be_called_if_hash_unchanged(self):
        """Feature extractor should only be re-computed when source changed."""
        test_extractor = me.MockExtractor('1', 'col_1', 42)
        test_extractor.extract = _CallCounterMock()

        # Create collection, add extractor and run (extract should be called).
        collection = fex.Collection(self.cache_file)
        collection.add_feature_extractor(test_extractor)
        collection.run(self.dataset_file)
        counter_first_run = test_extractor.extract.counter

        # Create a new collection with same extractor and run.
        collection2 = fex.Collection(self.cache_file)
        collection2.add_feature_extractor(test_extractor)
        collection2.run(self.dataset_file)
        self.assertEqual(counter_first_run, test_extractor.extract.counter)

    def test_collections_correctly_joins_dataframes(self):
        """Ensure the Mock FEX produces the correct DataFrame."""
        mex1 = me.MockExtractor('1', 'col_1', 100)
        mex2 = me.MockExtractor('1', 'col_2', 200)
        collection = fex.Collection()
        collection.add_feature_extractor(mex1)
        collection.add_feature_extractor(mex2)
        collection.run(self.dataset_file)
        contents = open(self.dataset_file).read().splitlines()
        expected = [
            ',MockExtractor__col_1,MockExtractor__col_2',
            '1,100,200'
        ]
        self.assertEqual(expected, contents)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
