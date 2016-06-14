"""A collection to execute a set of feature extractors."""

import collections
import logging
import os
import pandas as pd
import pickle

log = logging.getLogger('fex')


class Collection(object):
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
        features = self._generate_features(self._feature_extractors)
        features.to_csv(dataset_path)

    def _generate_features(self, feature_extractors):
        """Run all FeatureExtractors and record results in a key-value format.

        :param feature_extractors: iterable of `FeatureExtractor` objects.
        """
        results = [pd.DataFrame()]
        n_ext = len(feature_extractors)

        for i, extractor in enumerate(feature_extractors):
            log.info("generating: '%s' (%d/%d)", extractor.name, i + 1, n_ext)
            cached_extractor = self._cache[extractor.name]
            if extractor.same(cached_extractor):
                log.info('pulling from cache')
                extractor = cached_extractor
            else:
                log.info('running...')
                extractor.extract()
            results.append(extractor.result)
            if self.cache_path:
                self._cache[extractor.name] = extractor

        if self.cache_path:
            with open(self.cache_path, 'wb') as f:
                pickle.dump(self._cache, f)

        return pd.concat(results, axis=1)
