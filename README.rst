era5cli
=======

A command line interface to download ERA5 hydrological (sub)set. Currently the goal is to
have a copy of ERA5 available for eWaterCycle users.

**Comment:** downloading ERA5 all over again is not recommended as it will
be accessible via our platform. 

Installation:
-------------
era5cli is intallable via pip:
::

   pip3 install -U  git+https://github.com/eWaterCycle/era5cli.git


Instructions:
-------------

Register at Copernicus Climate Data Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  You have to register at Copernicus Climate Data Service:
   `copernicus <https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome>`__.
   After activating your account use your new account to log in. In you
   profile page you can find your user ID and your API key.

-  Copy your user ID and API key.

Create a key ascii file
~~~~~~~~~~~~~~~~~~~~~~~

In linux create a file called .cdsapirc in your home directory and add
the following two lines:

::

   url: https://cds.climate.copernicus.eu/api/v2

   key: UID:KEY 

Replace UID with your user ID and KEY with your API key


Run the python script from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   era5cli --years <years> --months <months> --days <days> --hours <hours> --variables <variable> --o <out.nc> --format <netcdf>


Optional arguments:
  -y, --years YEARS [YEARS ...]
                        Year(s) for which the data should be downloaded.
  -m, --months MONTHS [MONTHS ...]
                        Months to download data for. Defaults to all
                        months.
  -d, --days DAYS [DAYS ...] 
                        Days to download data for. Defaults to all days.
  -t, --hours HOURS [HOURS ...]
                        Time of day in hours to download data for.
                        Defaults to all hours.
  -p, --variables VARIABLES [VARIABLES ...]
                        The variable to be downloaded. See the cds
                        website for availabe variables.
  -o, --output OUTPUT [OUTPUT]
                        Name of output file. Defaults to 'output.nc'.
  -f, --format FORMAT [FORMAT]
                        Output file type. Defaults to 'netcdf'.



Available VARIABLES are listed in `ERA5 hourly data on single levels from
1979 to
present <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form>`__
(e.g., ‘total_precipitation’, ‘precipitation_type’, ‘snowfall’,
‘runoff’)
