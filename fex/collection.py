"""A collection to execute a set of feature extractors."""

import collections
# TODO: Get rid of heavy pandas dependency.
import pandas as pd
import logging
log = logging.getLogger('fex')


class FeatureExtractorCollection(object):
    """Framework to run FeatureExtractors."""

    def __init__(self):
        """Set up caching."""
        self._feature_extractors = []

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
            log.info("running: '%s' (%d/%d)", extractor.name, i + 1, n_ext)
            extractor.extract()
            # TODO Implement default iterator to do
            # `for row_id, values in extractor`
            for row_id, values in extractor._data_store.items():
                results[row_id].update(values)
        return pd.DataFrame.from_dict(results, orient='index')
