"""Expose FeatureExtractor directly on pex module and config logging."""

from fex.feature_extractor import FeatureExtractor # NOQA
from fex.feature_extractor_collection import FeatureExtractorCollection # NOQA
import logging
logging.basicConfig(format='%(levelname)s:%(name)s:%(asctime)s=> %(message)s',
                    datefmt='%m/%d %H:%M:%S',
                    level=logging.INFO)
