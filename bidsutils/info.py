import json
import os.path as op
import importlib.util

spec = importlib.util.spec_from_file_location(
    '_version', op.join(op.dirname(__file__), 'bidsutils/_version.py'))
_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_version)

VERSION = _version.get_versions()['version']
del _version

# Get list of authors from Zenodo file
with open(op.join(op.dirname(__file__), '.zenodo.json'), 'r') as fo:
    zenodo_info = json.load(fo)
authors = [author['name'] for author in zenodo_info['creators']]
authors = [author.split(', ')[1] + ' ' + author.split(', ')[0] for author in authors]

AUTHOR = 'FIU-Neuro developers'
COPYRIGHT = 'Copyright 2020--now, FIU-Neuro developers'
CREDITS = authors
LICENSE = 'MIT'
MAINTAINER = 'Taylor Salo'
EMAIL = 'tsalo006@fiu.edu'
STATUS = 'Prototype'
URL = 'https://github.com/FIU-Neuro/bidsutils'
PACKAGENAME = 'bidsutils'
DESCRIPTION = 'bidsutils: Functions for BIDS datasets'
LONGDESC = """
"""

DOWNLOAD_URL = (
    'https://github.com/FIU-Neuro/{name}/archive/{ver}.tar.gz'.format(
        name=PACKAGENAME, ver=VERSION))

REQUIRES = [
    'numpy',
    'scipy',
    'pandas',
    'pybids>=0.9.4'
]

TESTS_REQUIRES = [
    'codecov',
    'coverage',
    'coveralls',
    'flake8',
    'pytest',
    'pytest-cov'
]

DOC_REQUIRES = [
    'sphinx>=1.5.3',
    'sphinx_rtd_theme',
    'sphinx-argparse',
    'numpydoc',
    'm2r'
]

EXTRA_REQUIRES = {
    'doc': DOC_REQUIRES,
    'tests': TESTS_REQUIRES,
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES['all'] = list(set([
    v for deps in EXTRA_REQUIRES.values() for v in deps]))

ENTRY_POINTS = {}

# Package classifiers
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache 2.0 License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering'
]
