"""Feature Extractor base class."""

import collections
import hashlib
import inspect


class FeatureExtractor(object):
    """Class defining a feature extractor."""

    def __init__(self):
        """Prepare store which is used to collect the data.

        Attributes:
        - name: A string containing the name of the class.
        - prefix: Prefix used for column names. Modify to rename columns.
        """
        self.prefix = self.name = self.__class__.__name__
        self._data_store = collections.defaultdict(dict)
        class_source = inspect.getsource(self.__class__)
        self._source_hash = hashlib.md5(class_source.encode()).hexdigest()

    def same(self, other):
        """Compare two FeatureExtractor (FE) instances to each other.

        This comparator determines whether a FE has to be re-run by checking
        whether the underlying source code has changed. Override this method
        if you want to be more tolerant on caching.
        """
        if not other:
            return False
        return self._source_hash == other._source_hash

    def copy_to(self, results):
        """Copy values to results object of a FeatureExtractorCollection."""
        for row_id, values in self._data_store.items():
            results[row_id].update(values)

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
