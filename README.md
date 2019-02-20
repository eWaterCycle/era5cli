# pyERA5

Library to download ERA5 hydrological (sub)set.
Currently the goal is to have a copy of ERA5 available for eWaterCycle users.

This library is in a preliminary phase of development. 

## Hydrological Variables:

The following variables will be included in the eWatercycle data catalog.

  * Total precipitation
  * Precipitation type
  * 10m u-component of wind
  * 10m v-component of wind
  * 2m temperature
  * Skin temperature
  * 2m dewpoint temperature
  * Volumetric soil water layer 1
  * Potential evaporation
  * Evaporation
  * Surface net solar radiation
  * temperature of snowfall
  * snowfall
  * runoff


## Instructions:

Comment: downloading ERA5 all over again is not recommended as it will be accessible via our platform.
However, if you do want to download the data yourself (or use other vaiabiles than the ones we used) follow these steps:

### Register at Copernicus Climate Data Store

* You first have to register at Copernicus Climate Data Store: [copernicus](https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome). After activating your account use your new account to log in. In you profile page you can find your user ID and your API key.

* Copy your user ID and API key.

### Create a key ascii file

In linux create a file called .cdsapirc in your home directory and add the following two lines:

```
url: https://cds.climate.copernicus.eu/api/v2

key: UID:KEY 
```

Replace UID with your user ID and KEY with your API key 


### Install cdsapi

```
pip install cdsapi
```

### Run the python script from the command line

```
python3 pyera5_download.py Variable
```

Where Variable is one or more of the Hydrological variable(s): 'total_precipitation','precipitation_type','10m_u_component_of_wind','10m_v_component_of_wind', '2m_temperature', 'skin_temperature', '2m_dewpoint_temperature', 'volumetric_soil_water_layer_1','potential_evaporation','evaporation','top_net_solar_radiation_clear_sky','temperature_of_snow_layer', 'snowfall','runoff' 



