'''
description:    Download ERA5 from 
license:        APACHE 2.0
author:         Yifat Dzigan, NLeSC (y.dzigan@esciencecenter.nl)
'''

import cdsapi
import sys

HydroVariable_s = HydroVariable.split(",")

c = cdsapi.Client()
c.retrieve('reanalysis-era5-single-levels', {
        	'variable'      : HydroVariable_s,
        'product_type'  : 'reanalysis',
        'year'          : '2018',
        'month'         : ['02'],
        'day'           : '02',
        'time'          : '12:00',
        'format'        : 'netcdf' 
    }, 'test.nc')
