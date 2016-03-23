"""Feature Extractor base class."""

import collections
import hashlib
import inspect


class FeatureExtractor(object):
    """Class defining a feature extractor."""

    def __init__(self):
        """Prepare stores which are used to collect the data.

        The variable prefix can be overwritten to prefix all columns of
        a certain feature extractor
        """
        self.prefix = self.name = self.__class__.__name__
        self._data_store = collections.defaultdict(dict)
        source = inspect.getsource(self.__class__)
        self.hash = hashlib.md5(source.encode()).hexdigest()

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
