from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    '_version', Path(__file__).parent / '_version.py')
_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_version)

__version__ = _version.get_versions()['version']
del _version

__copyright__ = ('Copyright 2020--now, FIU-Neuro developers')
__credits__ = ['Taylor Salo', 'Adam Kimbler', 'Michael Riedel']
__packagename__ = 'cis-bidsutils'

DOWNLOAD_URL = (
    'https://github.com/FIU-Neuro/{name}/archive/{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__))
