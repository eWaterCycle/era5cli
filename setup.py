"""Hydro ERA5 download package."""
from setuptools import setup

with open('README.rst') as file:
    README = file.read()

setup(
    name="pyERA5",
    version="0.0.1",
    author="Jerom Aerts, Yifat Dzigan, Ronald van Haren",
    author_email=("J.P.M.Aerts@tudelft.nl, y.dzigan@esciencecenter.nl, "
                  "r.vanharen@esciencecenter.nl"),
    description=("A python library to download ERA5 "
                 "from the Copernicus Climate Data Store "
                 "https://climate.copernicus.eu/."),
    license="Apache 2.0",
    keywords="ERA5",
    url="https://github.com/ewatercycle/pyERA5",
    packages=['pyera5'],
    include_package_data=True,    # include everything in source control
    package_data={'pyera5': ['cartesius/*']},
    scripts=['pyera5/scripts/pyera5'],
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=['cdsapi'],
)
