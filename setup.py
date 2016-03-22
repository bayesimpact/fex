"""Bayes Impact feature extraction framework.

A simple feature extraction framework to extract data from different sources
and export them into an easy to share format.
"""

import setuptools

with open('requirements.txt') as file:
    requirements = file.readlines()

setuptools.setup(
    name='fex',
    version='0.0.1',
    packages=setuptools.find_packages()
)
