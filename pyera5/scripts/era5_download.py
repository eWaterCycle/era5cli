#!/usr/bin/env python

'''
description:    Download ERA5 from copernicus 
license:        APACHE 2.0Climate Data Store
author:         Jerom Aerts
'''

import cdsapi
import sys

#For slurm job arrays
taskid = int(sys.argv[1])
if taskid < 10:
  year = '200'+sys.argv[1]
else:
  year = '20'+sys.argv[1]


c = cdsapi.Client(key= "xxxx", url= "https://cds.climate.copernicus.eu/api/v2")
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'variable':'total_precipitation',
        'product_type':'reanalysis',
        'year':[year],
        'month':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12'
        ],
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        'format':'netcdf'
    },
    '/projects/0/wtrcycle/users/jaerts/era5_api_download/era5/total_precipitation/era5_total_precipitation_'+year+'.nc')