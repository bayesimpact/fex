"""Main module to run FeatureExtractor collections."""

import argparse
import logging
import os
import re
import subprocess
import sys

import fex

log = logging.getLogger('fex')


def _run_cmd_get_output(cmd):
    """Runs a shell command, returns console output.

    Mimics python3's subprocess.getoutput
    """
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out or err


def _remote_github_url_to_string(remote_url):
    """Parse out the repository identifier from a github URL."""
    # TODO: make this work with https URLs
    match = re.search('git@github\.com:(.*)\.git', remote_url)
    if not match:
        raise EnvironmentError('Remote is not a valid github URL')
    identifier = match.group(1)
    return re.sub('\W', ':', identifier)


def _get_git_remote():
    """Get remote branch as a unique identifier of the local git repository.

    returns: The URL of the remote branch, witout the username in it.
    raises: `EnvironmentError` if no remote set.
    """
    try:
        remote_url = _run_cmd_get_output('git ls-remote --get-url')
    except subprocess.CalledProcessError:
        raise EnvironmentError('No remote configured.')
    return _remote_github_url_to_string(remote_url)


def _git_is_pristine():
    """Check whether there are any uncommitted changes in the repository.

    returns: True if nothing uncommited in the repo or folder not a repo.
    raises: `EnvironmentError` if current directory is not a git repository.
    """
    command = 'git diff HEAD --shortstat'
    diff_str = _run_cmd_get_output(command)
    if "error: Could not access 'HEAD'" in diff_str:
        raise EnvironmentError('Not a git repository.')
    return diff_str == ''


def _get_git_hash():
    """Fetch the SHA-1 hash of the head commit and return first 12 digits.

    returns: The SHA-1 hash of the HEAD commit
    raises: `EnvironmentError` if current directory is not a git repository.
    """
    try:
        sha1_str = _run_cmd_get_output('git rev-parse --short=12 HEAD')
    except subprocess.CalledProcessError:
        raise EnvironmentError('Not a git repository.')

    return sha1_str.strip().lower()


def _get_args(args):
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


def _prefix_git_hash(out_path):
    # TODO: add unittests for this whole prefixing stuff
    try:
        if not _git_is_pristine():
            sys.exit('Cannot deploy: Commit all your changes first!')
        git_hash = _get_git_hash()
        git_remote = _get_git_remote()
    except EnvironmentError as e:
        sys.exit(e)
    path, filename = os.path.split(out_path)
    filename = ":".join([git_remote, git_hash, filename])
    return os.path.join(path, filename)


def run(*extractor_list, **kwargs):
    """Parse arguments provided on the commandline and execute extractors."""
    args = _get_args(kwargs.get('args'))
    n_extractors = len(extractor_list)
    log.info('Going to run list of {} FeatureExtractors'.format(n_extractors))
    collection = fex.Collection(cache_path=args.cache_path)
    for extractor in extractor_list:
        collection.add_feature_extractor(extractor)

    out_path = args.path
    if args.deploy:
        out_path = _prefix_git_hash(out_path)
    collection.run(out_path)
