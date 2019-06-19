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

In linux create a file called .cdsapirc in your home directory and add
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

              :samp:`plevels` for all available pressure levels 

              :samp:`slvars` for all available single level or 2D
              variables

              :samp:`plvars` for all available 3D variables 

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


::

   era5cli hourly --variables <variables> --startyear <startyear> --endyear <endyear> --months <months> --days <days> --hours <hours> --levels <levels> --outputprefix <outputprefix> --format <fileformat> --split <split> --threads <threads> --ensemble <ensemble> --statistics <statistics>

Execute the data fetch process for hourly data.

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
                        months. For every year in :samp:`--years` only these
                        months will be downloaded.
  --days DAYS
                        Day(s) to download data for. Defaults to all days.
                        For every year in :samp:`--years` only these days will
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
                        for every year in the :samp:`--years` argument. Default
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

::

   era5cli monthly --variables <variables> --startyear <startyear> --endyear <endyear> --months <months> --days <days> --hours <hours> --levels <levels> --outputprefix <outputprefix> --format <fileformat> --split <split> --threads <threads> --ensemble <ensemble> --synoptic <synoptic>

Execute the data fetch process for monthly data.

optional arguments:
  -h, --help            show this help message and exit
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
                        months. For every year in :samp:`--years` only these
                        months will be downloaded.
  --days DAYS
                        Day(s) to download data for. Defaults to all days.
                        For every year in :samp:`--years` only these days will
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
                        for every year in the :samp:`--years` argument. Default
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
  --synoptic SYNOPTIC   
                        Set :samp:`--synoptic True` to get monthly averaged
                        by hour of day or set :samp:`--synoptic False` to get
                        monthly means of daily means. Default is False.
