Instructions
------------

Register at Copernicus Climate Data Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  You have to register at Copernicus Climate Data Service:
   `copernicus <https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome>`__.
   After activating your account use your new account to log in. In you
   profile page you can find your user ID and your API key.

-  Copy your user ID and API key.

Create a key ascii file
~~~~~~~~~~~~~~~~~~~~~~~

In linux create a new file called .cdsapirc in the home directory of your user and add
the following two lines:

::

   url: https://cds.climate.copernicus.eu/api/v2

   key: UID:KEY 

Replace UID with your user ID and KEY with your API key

Info on available variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   era5cli info <name>

Show information on available variables and levels.

positional arguments:
 --name       Enter list name to print info list:

              :samp:`levels` for all available pressure levels 

              :samp:`2dvars` for all available single level or 2D
              variables

              :samp:`3dvars` for all available 3D variables 

              Enter variable name (e.g. "total_precipitation")
              or pressure level (e.g. "825") to show if the
              variable or level is available and in which list.

optional arguments:
  -h, --help  show this help message and exit


Running era5cli from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
era5cli can be used to fetch both hourly data and monthly averaged data.


Fetching hourly data
====================

Fetch hourly data through an cdsapi call via command line. More information on the available data and options can be found on:

| `Era5 hourly single levels download page <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview>`_.
| `Era5 hourly pressure levels download page <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview>`_.

Execute the data fetch process for hourly data:

::

   era5cli hourly --variables <variables> --startyear <startyear> --endyear <endyear> --months <months> --days <days> --hours <hours> --levels <levels> --outputprefix <outputprefix> --format <fileformat> --split <split> --threads <threads> --ensemble <ensemble> --statistics <statistics>

optional arguments:

  --variables VARIABLES

                        The variables to be downloaded, can be a single
                        or multiple variables. See the cds
                        website or run :samp:`era5cli info -h` for available variables.

  --startyear STARTYEAR

                        Single year or first year of range for which
                        data should be downloaded.
                        Every year will be downloaded in a seperate file
                        by default. Set :samp:`--split false` to change this.
  
  --endyear ENDYEAR

                        Last year of range for which  data should be
                        downloaded. If only a single year is needed, only
                        :samp:`--startyear` needs to be specified.
                        Every year will be downloaded in a seperate file
                        by default. Set :samp:`--split false` to change this.
  
  --months MONTHS

                        Month(s) to download data for. Defaults to all
                        months. For every year in :samp:`--years` only these
                        months will be downloaded.
  
  --days DAYS

                        Day(s) to download data for. Defaults to all days.
                        For every year in :samp:`--years` only these days will
                        be downloaded.
  
  --hours HOURS

                        Time of day in hours to download data for.
                        Defaults to all hours. Defaults to all hours. For every year only
                        these hours will be downloaded.
  
  --levels LEVELS

                        Pressure level(s) to download for three
                        dimensional data. Default is all available
                        levels. See the cds website or run :samp:`era5cli info
                        -h` for available pressure levels.
  
  --outputprefix OUTPUTPREFIX

                        Prefix of output filename. Default prefix is
                        "era5".

  --format FORMAT

                        Choose from :samp:`[netcdf,grib]`.

                        Output file type. Defaults to :samp:`netcdf`."

  --split SPLIT

                        Split output by years, producing a seperate file for every year
                        instead of merging in one file. D Default
                        is True.

  --threads THREADS

                        Choose from :samp:`[1,2,3,4,5,6]`.

                        Number of parallel threads to use when
                        downloading. Default is a single process.
  
  --ensemble ENSEMBLE

                        Whether to download high resolution realisation
                        (HRES) or a reduced resolution ten member ensemble
                        (EDA). :samp:`--ensemble True` downloads the reduced
                        resolution ensemble.

  --statistics STATISTICS
                        
                        When downloading hourly ensemble data, set
                        :samp:`--statistics True` to download statistics
                        (ensemble mean and ensemble spread). Default is
                        False.

  -h, --help            show this help message and exit


Fetching monthly data
=====================

Fetch monthly data through an cdsapi call via command line. More information on the available data and options can be found on:

| `Era5 monthly single levels download page <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=overview>`_.
| `Era5 monthly pressure levels download page <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels-monthly-means?tab=overview>`_.

For the monthly data, some of the variables are not available. Exceptions on the single level data can be found in table 8 of:

| `ERA5 parameter listings <https://confluence.ecmwf.int/display/CKB/ERA5+data+documentation#ERA5datadocumentation-Parameterlistings>`_

Execute the data fetch process for monthly data:

::

   era5cli monthly --variables <variables> --startyear <startyear> --endyear <endyear> --months <months> --hours <hours> --levels <levels> --outputprefix <outputprefix> --format <fileformat> --split <split> --threads <threads> --ensemble <ensemble> --synoptic <synoptic>

optional arguments:

  --variables VARIABLES

                        The variables to be downloaded, can be a single
                        or multiple variables. See the cds
                        website or run :samp:`era5cli info -h` for available
                        variables.

  --startyear STARTYEAR
 
                        Single year or first year of range for which
                        data should be downloaded.
                        Every year will be downloaded in a seperate file
                        by default. Set :samp:`--split false` to change this.

  --endyear ENDYEAR
 
                        Last year of range for which  data should be
                        downloaded. If only a single year is needed, only
                        :samp:`--startyear` needs to be specified.
                        Every year will be downloaded in a seperate file
                        by default. Set :samp:`--split false` to change this.

  --months MONTHS

                        Month(s) to download data for. Defaults to all
                        months. For every year only these
                        months will be downloaded.

  --days DAYS

                        Day(s) to download data for. Defaults to all days.
                        For every year only these days will
                        be downloaded.

  --hours HOURS

                        Time of day in hours to download data for.
                        Defaults to all hours. For every year in
                        :samp:`--years` only these hours will be downloaded.

  --levels LEVELS

                        Pressure level(s) to download for three
                        dimensional data. Default is all available
                        levels. See the cds website or run :samp:`era5cli info
                        -h` for available pressure levels.

  --outputprefix OUTPUTPREFIX
 
                        Prefix of output filename. Default prefix is
                        "era5".

  --format FORMAT

                        Choose from :samp:`[netcdf,grib]`.

                        Output file type. Defaults to :samp:`netcdf`."

  --split SPLIT

                        Split output by years, producing a seperate file
                        for every year instead of mergin in one file. Default is True.

  --threads THREADS
 
                        Choose from :samp:`[1,2,3,4,5,6]`.

                        Number of parallel threads to use when
                        downloading. Default is a single process.

  --ensemble ENSEMBLE
 
                        Whether to download high resolution realisation
                        (HRES) or a reduced resolution ten member ensemble
                        (EDA). :samp:`--ensemble True` downloads the reduced
                        resolution ensemble.

  --synoptic SYNOPTIC
 
                        Set :samp:`--synoptic True` to get monthly averaged
                        by hour of day or set :samp:`--synoptic False` to get
                        monthly means of daily means. Default is False.

  -h, --help            show this help message and exit