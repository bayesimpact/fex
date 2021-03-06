"""Bayes Impact feature extraction framework.

A simple feature extraction framework to extract data from different sources
and export them into an easy to share format.
"""

import os
from pip.req import parse_requirements
import setuptools
import sys


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


def dist_pypi():
    """Publish current version to Pypi."""
    os.system("python setup.py sdist upload")
    sys.exit()


if 'publish' in sys.argv:
    if '--manual-tests-done' in sys.argv:
        dist_pypi()
    else:
        sys.exit('Please run manual tests described in tests/manual_tests.md')


setuptools.setup(
    name='fex',
    description=__doc__,
    version='0.2.0',
    packages=['fex'],
    author='Stephan Gabler',
    author_email='stephan@bayesimpact.org',
    url='https://github.com/bayesimpact/fex',
    license='The MIT License (MIT)',
    keywords=['feature extraction', 'framework'],
    install_requires=reqs
)
