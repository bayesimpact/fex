"""Main module to run FeatureExtractor collections."""

import argparse
import logging
from fex import FeatureExtractorCollection
log = logging.getLogger('fex')


def get_args(args):
    """Argparse logic lives here.

    :returns: parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='A tool to extract features into a simple format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--cache-path', type=str, default='fex-cache.pckl',
                        help='Path for cache file')
    parser.add_argument('--path', type=str, default='features.csv',
                        help='Path to write the dataset to')
    return parser.parse_args(args)


def run(*extractor_list, **kwargs):
    """Parse arguments provided on the commandline and execute extractors."""
    args = get_args(kwargs.get('args'))
    n_extractors = len(extractor_list)
    log.info('Going to run list of {} FeatureExtractors'.format(n_extractors))
    if args.no_cache:
        args.cache_path = None
    collection = FeatureExtractorCollection(cache_path=args.cache_path)
    for extractor in extractor_list:
        collection.add_feature_extractor(extractor)
    collection.run(args.path)
