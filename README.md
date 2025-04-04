[![github license badge](https://img.shields.io/github/license/eWaterCycle/era5cli)](https://github.com/eWaterCycle/era5cli)
[![rsd badge](https://img.shields.io/badge/RSD-era5cli-blue)](https://research-software-directory.org/software/era5cli)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3252665.svg)](https://doi.org/10.5281/zenodo.3252665)

[![Documentation Status](https://readthedocs.org/projects/era5cli/badge/?version=stable)](https://era5cli.readthedocs.io/en/stable/?badge=stable)
[![build](https://github.com/eWaterCycle/era5cli/actions/workflows/test_and_build.yml/badge.svg)](https://github.com/eWaterCycle/era5cli/actions/workflows/test_and_build.yml)
[![Test Coverage](https://codecov.io/gh/eWaterCycle/era5cli/branch/main/graph/badge.svg?token=qeZXgGASBK)](https://codecov.io/gh/eWaterCycle/era5cli)
[![PyPI](https://badge.fury.io/py/era5cli.svg)](https://badge.fury.io/py/era5cli)

<img align="right" width="150" alt="Logo" src="docs/assets/era5cli_logo_colors_border.png">

> [!IMPORTANT]
> The old Climate Data Store (CDS) has been shut down. All era5cli versions up to v1.4.2 will no longer work.
> 
> For more information see:
> https://forum.ecmwf.int/t/goodbye-legacy-climate-data-store-hello-new-climate-data-store-cds/6380/14
> 
> To continue using era5cli, you will need to re-register at ECMWF and get a new API key,
> and transition to era5cli version 2. This can be installed with:
> `pip install era5cli==2.0.1` 

> [!WARNING]
> netCDF files from the new Climate Data Store Beta are not formatted the same as the
> old CDS. Some variables might be missing.
> See the open issue [here](https://github.com/eWaterCycle/era5cli/issues/165), as well as the [ECMWF discussion forum](https://forum.ecmwf.int/).  

A command line interface to download ERA5 data from the [Copernicus Climate Data Store](<https://climate.copernicus.eu/>).

<hr>

With `era5cli` you can:

 - Download meteorological data in GRIB/NetCDF, including ERA5 data from the preliminary back extension, and ERA5-Land data.
 - List and retrieve information on available variables and pressure levels
 - Select multiple variables for several months and years
 - Split outputs by years (and optionally months), producing a separate files instead of merging them in one file
 - Download multiple files at once
 - Extract data for a sub-region of the globe

<hr>

Free software: Apache Software License 2.0

Documentation: https://era5cli.readthedocs.io

