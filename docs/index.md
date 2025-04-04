# Welcome to era5cli’s documentation!

A command line interface to download ERA5 data from the [Copernicus Climate Data Store](https://climate.copernicus.eu/).

???+ note
    The old Climate Data Store (CDS) will be shut down on 3 September 2024.
    All era5cli versions up to v1.4.2 will no longer work.
   
    For more information see: https://forum.ecmwf.int/t/the-new-climate-data-store-beta-cds-beta-is-now-live/3315
   
    To continue using era5cli, you will need to re-register at ECMWF and get a new API key,
    and transition to the era5cli v2 beta. This can be installed with:
    `pip install era5cli>=2.0.1` 

???+ warning
    netCDF files from the new Climate Data Store Beta are not formatted the same as the
    old CDS. Some variables might be missing.
    
    See the open issue [here](https://github.com/eWaterCycle/era5cli/issues/165), as well as the [ECMWF discussion forum](https://forum.ecmwf.int/).

With era5cli you can:

 - Download meteorological data in GRIB/NetCDF, including ERA5 data from the preliminary back extension, and ERA5-Land data.
 - List and retrieve information on available variables and pressure levels
 - Select multiple variables for several months and years
 - Split outputs by years (and optionally months), producing a separate files instead of merging them in one file
 - Download multiple files at once
 - Extract data for a sub-region of the globe

For information on how to use era5cli, please go to the [user guide](getting_started.md).