"""Fetch ERA5 variables."""

import cdsapi
# from pathos.multiprocessing import ProcessPool as Pool
from pathos.threading import ThreadPool as Pool

from variables import slvars, plvars

class Fetch:
    """Fetch ERA5 data using cdsapi."""

    def __init__(self, pressurelevels=None, years, months, days, hours, variables, outputformat,
                 outputprefix, split=True, threads=None):
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
        if split:
            # split by variable and year
            self.split_variable_yr()
        else:
            #split by variable
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

    def define_outputfile(outputprefix, variable, year):
        outputfile = "{}_{}_{}.{}".format(self.outputprefix,
                                          variable,
                                          year, self.ext)
        return outputfile

    def getdata(self, variable, years, outputfile):
        """Fetch variables using cds api call."""
        c = cdsapi.Client()

        if variable in slvars:
            c.retrieve('reanalysis-era5-single-levels',
                       {'variable': variable,
                        'product_type': 'reanalysis',
                        'year': years,
                        'month': self.months,
                        'day': self.days,
                        'time': self.hours,
                        'format': self.outputformat},
                       outputfile)

        elif variable in plvars:
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
            raise Exception('Invalid variable name: {}'.format{variable})
