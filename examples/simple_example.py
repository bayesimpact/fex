#!/usr/bin/env python
"""Simple example of runner usage.

This example demonstrates how to implement custom Feature extractor classes
and how they can be executed using the fex runner.

The runner has sensible defaults for arguments which can be modified via
commandline arguments. For details call this file with `-h` or `--help`.

    examples/simple_example.py --help
"""

import fex
from fex import runner
import logging
logging.basicConfig(format='%(levelname)s:%(name)s:%(asctime)s=> %(message)s',
                    datefmt='%m/%d %H:%M:%S',
                    level=logging.INFO)


class ExampleFeature1(fex.FeatureExtractor):
    """First example feature extractor, super cool."""

    def extract(self):
        """Overriden method with custom logic.

        This is the place where one would do the data extraction and
        transformation.
        """
        self.emit(1, 'col1', 666)


class ExampleFeature2(fex.FeatureExtractor):
    """Another example feature extractor."""

    def extract(self):
        """Overriden method with custom logic."""
        self.emit(2, 'col1', 42)
        self.emit(2, 'col2', 314)

runner.run(ExampleFeature1(), ExampleFeature2())
