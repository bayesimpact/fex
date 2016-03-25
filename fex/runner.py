"""Main module to run FeatureExtractor collections."""

import argparse
import logging
import os
import re
import subprocess
import sys

from fex import FeatureExtractorCollection

log = logging.getLogger('fex')


def _remote_github_url_to_string(remote_url):
    """Parse out the repository identifier from a github URL."""
    match = re.search('git@github\.com:(.*)\.git', remote_url)
    if not match:
        log.warn('Remote is not a valid github URL')
        return ''
    else:
        identifier = match.group(1)
        return re.sub('\W', ':', identifier)


def get_git_remote():
    """Get remote branch as a unique identifier of the local git repository.

    returns: The URL of the remote branch, witout the username in it.
    raises: `ValueError` if current directory is not a git repository.
    """
    try:
        remote_url = subprocess.getoutput('git ls-remote --get-url')
        return _remote_github_url_to_string(remote_url)
    except subprocess.CalledProcessError:
        raise ValueError('No remote configured.')


def git_is_pristine():
    """Check whether there are any uncommitted changes in the repository.

    returns: True if nothing uncommited in the repo or folder not a repo.
    """
    command = "git diff HEAD --shortstat 2> /dev/null | tail -n1"
    diff_str = subprocess.getoutput(command)
    return diff_str == ''


def get_git_hash():
    """Fetch the SHA-1 hash of the head commit and return first 12 digits.

    returns: The SHA-1 hash of the HEAD commit
    raises: `ValueError` if current directory is not a git repository.
    """
    try:
        sha1_str = subprocess.getoutput('git rev-parse HEAD')
    except subprocess.CalledProcessError:
        raise ValueError('Not a git repository.')

    sha1_str = sha1_str.strip().lower()[:12]
    return sha1_str


def get_args(args):
    """Argparse logic lives here.

    returns: parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='A tool to extract features into a simple format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--deploy', action='store_true')
    parser.add_argument('--cache-path', type=str, default='fex-cache.pckl',
                        help='Path for cache file')
    parser.add_argument('--path', type=str, default='features.csv',
                        help='Path to write the dataset to')
    args = parser.parse_args(args)
    if args.no_cache:
        args.cache_path = None
    return args


def run(*extractor_list, **kwargs):
    """Parse arguments provided on the commandline and execute extractors."""
    args = get_args(kwargs.get('args'))
    n_extractors = len(extractor_list)
    log.info('Going to run list of {} FeatureExtractors'.format(n_extractors))
    collection = FeatureExtractorCollection(cache_path=args.cache_path)
    for extractor in extractor_list:
        collection.add_feature_extractor(extractor)

    out_path = args.path
    if args.deploy:
        if not git_is_pristine():
            sys.exit('Cannot deploy: Commit all your changes first!')
        try:
            git_hash = get_git_hash()
            git_remote = get_git_remote()
        except ValueError as e:
            sys.exit(e.message)
        path, filename = os.path.split(out_path)
        filename = ":".join([git_remote, git_hash, filename])
        out_path = os.path.join(path, filename)
    collection.run(out_path)
