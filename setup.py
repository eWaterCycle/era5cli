import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyERA5",
    version="0.0.1",
    author="Jerom Aerts",
    author_email="J.P.M.Aerts@tudelft.nl",
    description=("A python library to download ERA5 "
                 "from the Copernicus Climate Data Store https://climate.copernicus.eu/."),
    license="Apache 2.0",
    keywords="ERA5",
    url="https://github.com/ewatercycle/pyERA5",
    packages=['pyERA5'],
    include_package_data=False,    # include everything in source control
    scripts=['pyera5/scripts/pyera5'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=['cdsapi'],
)
