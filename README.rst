Hydrological-ERA5-download
==========================

Library to download ERA5 hydrological (sub)set. Currently the goal is to
have a copy of ERA5 available for eWaterCycle users.

Hydrological Variables:
-----------------------

The following variables will be included in the eWatercycle data
catalog.

-  Total precipitation
-  Precipitation type
-  10m u-component of wind
-  10m v-component of wind
-  2m temperature
-  Skin temperature
-  2m dewpoint temperature
-  Volumetric soil water layer 1
-  Potential evaporation
-  Evaporation
-  Surface net solar radiation
-  temperature of snowfall
-  snowfall
-  runoff
-  surface solar radiation downwards
-  toa incident solar radiation
-  mean sea level pressure
-  orography

Instructions:
-------------

Comment: downloading ERA5 all over again is not recommended as it will
be accessible via our platform. However, if you do want to download the
data yourself (or use other vaiabiles than the ones we used) follow
these steps:

Register at Copernicus Climate Data Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  You first have to register at Copernicus Climate Data Service:
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

Install cdsapi
~~~~~~~~~~~~~~

::

   pip install cdsapi

Run the python script from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   python3 pyera5_download.py --years 2017,2018 --variable runoff

Where you can choose the variable you would like to download and the
years (can be a single year or a comma separated list):

Available variables are listed in `ERA5 hourly data on single levels from
1979 to
present <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form>`__
(e.g., ‘total_precipitation’, ‘precipitation_type’, ‘snowfall’,
‘runoff’)
