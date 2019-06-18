"""Fetch ERA5 variables."""

import cdsapi
# from pathos.multiprocessing import ProcessPool as Pool
from pathos.threading import ThreadPool as Pool
import era5cli.inputref as ref

from variables import slvars, plvars

class Fetch:
    """Fetch ERA5 data using cdsapi."""

<<<<<<< HEAD
    def __init__(self,  years, months, days, hours, variables, outputformat,
                 outputprefix, pressurelevels=ref.plevels, split=True,
                 threads=None):
=======
    def __init__(self, pressurelevels=None, years, months, days, hours, variables, outputformat,
                 outputprefix, split=True, threads=None):
>>>>>>> a33c3fa7eedb1ec821dc9b33178652e167dec17f
        """Initialization of Fetch class."""
        self.months = months
        self.days = days
        self.hours = hours
        self.pressurelevels = pressurelevels
        self.variables = variables
        self.outputformat = outputformat
        self.years = years
        self.outputprefix = outputprefix
        self.threads = threads
        self.split = split

        # define extension output filename
        self.extension()

    def fetch(self):
        """Split calls and fetch results."""
<<<<<<< HEAD
        if self.split:
            # split by variable and year
            self.split_variable_yr()
        else:
            # split by variable
=======
        if split:
            # split by variable and year
            self.split_variable_yr()
        else:
            #split by variable
>>>>>>> a33c3fa7eedb1ec821dc9b33178652e167dec17f
            self.split_variable()

    def extension(self):
        """Set filename extension."""
        if (self.outputformat.lower() == 'netcdf'):
            self.ext = "nc"
        elif (self.outputformat.lower() == 'grib'):
            self.ext = 'grb'
        else:
            raise Exception('Unknown outputformat: {}'.format(
                            self.outputformat))

    def split_variable(self):
        """Split by variable."""
        outputfiles = ["{}_{}.{}".format(self.outputprefix, var, self.ext)
                       for var in self.variables]
        years = len(outputfiles) * [self.years]
        if not self.threads:
            pool = Pool()
        else:
            pool = Pool(nodes=self.threads)
        pool.map(self.getdata, self.variables, years, outputfiles)

    def split_variable_yr(self):
        """Fetch variable split by variable and year."""
        outputfiles = []
        years = []
        variables = []
        for var in self.variables:
            outputfiles += ["{}_{}_{}.{}".format(self.outputprefix, var, yr,
                                                 self.ext) for yr in
                            self.years]
            years += [yr for yr in self.years]
            variables += len(outputfiles) * [var]
        if not self.threads:
            pool = Pool()
        else:
            pool = Pool(nodes=self.threads)
        pool.map(self.getdata, variables, years, outputfiles)

    def getdata(self, variable, years, outputfile):
        """Fetch variables using cds api call."""
        c = cdsapi.Client()

        if variable in ref.slvars:
            c.retrieve('reanalysis-era5-single-levels',
                       {'variable': variable,
                        'product_type': 'reanalysis',
                        'year': years,
                        'month': self.months,
                        'day': self.days,
                        'time': self.hours,
                        'format': self.outputformat},
                       outputfile)

        elif variable in ref.plvars:
            if all([l in ref.plevels for l in self.pressure_levels]):
                c.retrieve('reanalysis-era5-pressure-levels',
                           {'variable': variable,
                            'pressure_level': self.pressure_levels,
                            'product_type': 'reanalysis',
                            'year': years,
                            'month': self.months,
                            'day': self.days,
                            'time': self.hours,
                            'format': self.outputformat},
                           outputfile)
            else:
                raise Exception('''
                    Invalid pressure levels. Allowed values are: {}
                    '''.format(ref.plevels))
        else:
            raise Exception('Invalid variable name: {}'.format(variable))
