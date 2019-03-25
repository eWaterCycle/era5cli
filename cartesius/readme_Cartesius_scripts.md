This library contains scripts used to download ERA5 to Cartesius: the Dutch supercomputer

The bash file era5_job_array.sh creates a job array on Cartesius and allows for specifying variable names through system arguments. These variable names need to comply with the ERA5 dataset. The bash file calls era5_download.py which is the generic python api script from Copernicus with a modification that allows for system arguments.

Please insert your own API key available from: https://cds.climate.copernicus.eu/cdsapp#!/home
