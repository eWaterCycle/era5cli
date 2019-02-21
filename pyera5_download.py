'''
description:    Download ERA5 from 
license:        APACHE 2.0
author:         Yifat Dzigan, NLeSC (y.dzigan@esciencecenter.nl)
'''

from optparse import OptionParser
import sys
import cdsapi
import re


usage = """Usage:

    --years <years> --variable <variable> 

    Examples:

    runoff for the year 2018
    >>> python3 --years 2018 --variable runoff

    runoff for 2017 and 2018
    >>> python3 --years 2017,2018 --variable runoff

    
""".format(__file__)
parser = OptionParser(usage = usage)
parser.add_option("-y", "--years", dest = "years", type = "str",
        help="years for which the data should be downloaded. " + \
                 "Can be a single year or a comma separated list ")
parser.add_option("-p", "--variable", dest = "var", type = "str",
       help="the variable to be downloaded. See the cds website for availabe variables.")
(options,args) = parser.parse_args()


if options.years == None or options.var == None:
    parser.print_help(); sys.exit(9)
else:
    if re.match("^[0-9]{4}$", options.years):
        options.years = [int(options.years)]
    elif re.match("^[0-9,]+$", options.years):
        options.years = [int(x) for x in options.years.split(",")]
    else:
        parser.print_help(); log.info("\n\n")
        raise ValueError("Wrong format for -y/--years")

HydroVariable = options.var
years = options.years

c = cdsapi.Client()
c.retrieve('reanalysis-era5-single-levels', {
        	'variable'      : HydroVariable,
        'product_type'  : 'reanalysis',
        'year'          : years,
        'month'         : ['01','02','03','04','05','06',
            		   '07','08','09','10','11','12'],
        'day'           : '01',
        'time'          : [
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        'format'        : 'netcdf' 
    }, 'test.nc')


