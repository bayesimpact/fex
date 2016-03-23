"""Tests for the fex FeatureExtractor."""

from fex import FeatureExtractor


ROW_ID = '1'
COLUMN_NAME = 'test_col'


class TestExtractor(FeatureExtractor):
    """A very simple test extractor."""

    def extract(self):
        """Overriden method to emit data."""
        self.emit(ROW_ID, COLUMN_NAME, 42)


def column_naming_test():
    """Column name should be a combination of FeatureExtractor and column name."""
    test_extractor = TestExtractor()
    test_extractor.extract()
    row = test_extractor._data_store[ROW_ID]
    col_name = list(row.keys())[0]
    assert col_name.startswith(TestExtractor.__name__)
    assert col_name.endswith(COLUMN_NAME)
