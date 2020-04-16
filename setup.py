#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""BIDSUTILS setup script."""
from setuptools import setup

if __name__ == '__main__':
    import versioneer
    from bidsutils.__about__ import __version__, DOWNLOAD_URL

    setup(
        name='bidsutils',
        version=__version__,
        cmdclass=versioneer.get_cmdclass(),
        download_url=DOWNLOAD_URL
    )
