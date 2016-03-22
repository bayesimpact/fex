"""A collection to execute a set of feature extractors."""

import collections
import pandas as pd
import logging
log = logging.getLogger('fex')


class FeatureExtractorCollection(object):
    """Framework to run FeatureExtractors."""

    def __init__(self):
        """Set up caching."""
        self.feature_extractors_ = []

    def add_feature_extractor(self, feature_extractor):
        """Add a new FeatureExtractor to the framework."""
        self.feature_extractors_.append(feature_extractor)

    def run(self, dataset_path):
        """Run all FeatureExtractors and output results to CSV."""
        features = self.generate_features(self.feature_extractors_)
        features.index.name = 'row_id'
        features.to_csv(dataset_path)

    def generate_features(self, feature_extractors):
        """Run all FeatureExtractors and record results in a key-value format.

        :param feature_extractors: iterable of :class:`FeatureExtractor` objects.
        """
        results = collections.defaultdict(dict)
        n_ext = len(feature_extractors)

        for i, extractor in enumerate(feature_extractors):
            info_str = "'{}' ({}/{})".format(extractor.name, i + 1, n_ext)
            log.info('running: ' + info_str)
            extractor.extract()
            # TODO Implement default iterator to do `for row_id, values in extractor`
            for row_id, values in extractor._data_store.items():
                results[row_id].update(values)
        # TODO: Get rid of heavy pandas dependency.
        return pd.DataFrame.from_dict(results, orient='index')
