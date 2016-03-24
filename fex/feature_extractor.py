"""Feature Extractor base class."""

import collections
import hashlib
import inspect


class FeatureExtractor(object):
    """Class defining a feature extractor."""

    def __init__(self):
        """Prepare stores which are used to collect the data.

        Attributes:
        - name: A string containing the name of the class.
        - prefix: Prefix used for column names. Modify to rename columns.
        """
        self.prefix = self.name = self.__class__.__name__
        self._data_store = collections.defaultdict(dict)

    def same(self, other):
        """Compare two FeatureExtractor (FE) instances to each other.

        This comparator determines whether a FE has to be re-run by checking
        whether the underlying source code has changed. Override this method
        if you want to be more tolerant on caching.
        """
        if not other:
            return False
        own_source = inspect.getsource(self.__class__)
        own_hash = hashlib.md5(own_source.encode()).hexdigest()
        other_source = inspect.getsource(other.__class__)
        other_hash = hashlib.md5(other_source.encode()).hexdigest()
        return own_hash == other_hash

    def iterrows(self):
        """Iterate over all rows in the datastore.

        Returns: (row_id, values) tuples.
        """
        for row_id, values in self._data_store.items():
            yield row_id, values

    def extract(self):
        """Override this function."""
        raise NotImplementedError

    def emit(self, row_id, feature_id, value):
        """Use this function in emit data into the store.

        :param row_id: string uniquely identifying the row.
        :param feature_id: string uniquely identifying the column.
        :param value: value to be recorded.
        """
        row_id = str(row_id)
        feature_id = self.prefix + '__' + str(feature_id)
        self._data_store[row_id][feature_id] = value
