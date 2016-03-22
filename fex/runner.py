"""Main module to run FeatureExtractor collections."""

import argparse
import logging
from fex import FeatureExtractorCollection
log = logging.getLogger('fex')


def get_args():
    """Argparse logic lives here.

    :returns: parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='A tool to extract features into a simple format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--path', type=str, default='features.csv',
                        help='Path to write the dataset to')
    return parser.parse_args()


def run(*extractor_list):
    """Parse arguments provided on the commandline and execute extractors."""
    args = get_args()
    n_extractors = len(extractor_list)
    log.info('Going to run list of {} FeatureExtractors'.format(n_extractors))
    collection = FeatureExtractorCollection()
    for extractor in extractor_list:
        collection.add_feature_extractor(extractor)
    collection.run(args.path)
