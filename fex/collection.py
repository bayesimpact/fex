"""A collection to execute a set of feature extractors."""

import collections
import os
import pickle

# TODO: Get rid of heavy pandas dependency.
import pandas as pd
import logging

log = logging.getLogger('fex')


class FeatureExtractorCollection(object):
    """Framework to run FeatureExtractors."""

    def __init__(self, cache_path=None):
        """Set up caching."""
        self._feature_extractors = []
        self.cache_path = cache_path
        if self.cache_path and os.path.exists(self.cache_path):
            self._cache = pickle.load(open(self.cache_path, 'rb'))
        else:
            self._cache = collections.defaultdict(dict)

    def add_feature_extractor(self, feature_extractor):
        """Add a new FeatureExtractor to the framework."""
        self._feature_extractors.append(feature_extractor)

    def run(self, dataset_path):
        """Run all FeatureExtractors and output results to CSV."""
        features = self.generate_features(self._feature_extractors)
        features.index.name = 'row_id'
        features.to_csv(dataset_path)

    def generate_features(self, feature_extractors):
        """Run all FeatureExtractors and record results in a key-value format.

        :param feature_extractors: iterable of `FeatureExtractor` objects.
        """
        results = collections.defaultdict(dict)
        n_ext = len(feature_extractors)

        for i, extractor in enumerate(feature_extractors):
            info_str = "'{}' ({}/{})".format(extractor.name, i + 1, n_ext)
            cached_extractor = self._cache[extractor.name]
            if cached_extractor and extractor.hash == cached_extractor.hash:
                log.info('from cache: ' + info_str)
                # TODO Implement default iterator to do
                # `for row_id, values in extractor`
                for row_id, values in cached_extractor._data_store.items():
                    results[row_id].update(values)
            else:
                log.info('running: ' + info_str)
                extractor.extract()
                # TODO Implement default iterator to do
                # `for row_id, values in extractor`
                for row_id, values in extractor._data_store.items():
                    results[row_id].update(values)
                if self.cache_path:
                    self._cache[extractor.name] = extractor

        if self.cache_path:
            with open(self.cache_path, 'wb') as f:
                pickle.dump(self._cache, f)

        return pd.DataFrame.from_dict(results, orient='index')
