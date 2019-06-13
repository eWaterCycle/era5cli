"""Hydro ERA5 download package."""
from setuptools import setup

with open('README.rst') as file:
    README = file.read()

setup(
    name="era5cli",
    version="0.0.1",
    author="Ronald van Haren, Yifat Dzigan, Jaro Camphuijsen, Jerom Aerts ",
    author_email=("r.vanharen@esciencecenter.nl"),
    description=("A python library to download ERA5 "
                 "from the Copernicus Climate Data Store "
                 "https://climate.copernicus.eu/."),
    license="Apache 2.0",
    keywords="ERA-5",
    url="https://github.com/ewatercycle/era5cli",
    packages=['era5cli'],
    include_package_data=True,    # include everything in source control
    package_data={'era5cli': ['cartesius/*']},
    #scripts=['era5cli/scripts/era5cli'],
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=['cdsapi', 'pathos'],
    entry_points={'console_scripts': [
        'era5cli=era5cli.cli:main']}
)
