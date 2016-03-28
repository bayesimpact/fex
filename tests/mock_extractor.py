"""Example classes to use in several tests."""

import fex


class MockExtractor(fex.FeatureExtractor):
    """A very simple test extractor."""

    def __init__(self, row_id, col_name, value):
        """Remember values to make tests more readable."""
        super(MockExtractor, self).__init__()
        self.row_id = row_id
        self.col_name = col_name
        self.value = value

    def extract(self):
        """Overriden method to emit data."""
        self.emit(self.row_id, self.col_name, self.value)
