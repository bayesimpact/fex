"""Bayes Impact feature extraction framework.

A simple feature extraction framework to extract data from different sources
and export them into an easy to share format
"""

from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.readlines()

print(find_packages())

setup(
    name='fex',
    version='0.0.1',
    packages=find_packages()
)
