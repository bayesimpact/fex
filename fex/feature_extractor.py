"""Feature Extractor base class."""

import hashlib
import inspect


class FeatureExtractor(object):
    """Base class for all feature extractors."""

    def __init__(self):
        """Prepare store which is used to collect the data.

        Attributes:
        - name: A string containing the name of the class.
        - prefix: Prefix used for column names. Modify to rename columns.
        """
        self.prefix = self.name = self.__class__.__name__
        self.result = None
        try:
            class_source = inspect.getsource(self.__class__)
        except TypeError:
            # Object created in python console -- hard to get its source.
            class_source = ''
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
        if self.result is not None:
            raise MultipleEmitsError()
        data_frame.columns = [self.prefix + '__' + c
                              for c in data_frame.columns]
        self.result = data_frame


class FeatureExtractorBaseException(Exception):
    """Base class for all fex-specific exceptions."""

    pass


class MultipleEmitsError(FeatureExtractorBaseException):
    """Exception when a Fex tries to emit (set its result) more than once."""

    def __init__(self):
        """Constructor."""
        Exception.__init__(self, "Can only emit once per feature extractor.")
