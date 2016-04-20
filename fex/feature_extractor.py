"""Feature Extractor base class."""

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
        self.result = None
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

    def extract(self):
        """Override this function."""
        raise NotImplementedError

    def emit(self, data_frame):
        """Use this function in emit data into the store.

        :param data_frame: DataFrame to be recorded.
        """
        data_frame.columns = [self.prefix + '__' + c
                              for c in data_frame.columns]
        self.result = data_frame
