#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGELOG.rst')).read()

about = {}
with open(os.path.join(here, 'era5cli', '__version__.py'), 'r') as f:
    exec(f.read(), about)

reqs = [line.strip() for line in open('requirements.txt')]

setup(
    name="era5cli",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    description=("A command line interface to download ERA5 data "
                 "from the Copernicus Climate Data Store "
                 "https://climate.copernicus.eu/."),
    license="Apache 2.0",
    keywords="ERA-5",
    url="https://github.com/ewatercycle/era5cli",
    packages=find_packages(),
    include_package_data=True,    # include everything in source control
    long_description=README,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=reqs,
    entry_points={'console_scripts': [
        'era5cli=era5cli.cli:main']}
)
