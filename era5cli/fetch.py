"""Fetch ERA5 variables."""

import cdsapi
# from pathos.multiprocessing import ProcessPool as Pool
from pathos.threading import ThreadPool as Pool

from variables import slvars, plvars

class Fetch:
    """Fetch ERA5 data using cdsapi."""

    def __init__(self, pressurelevels=None, years, months, days, hours, variables, outputformat,
                 outputprefix, split=['variable', 'year'], threads=None):
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
        # fetch files
        try:
            if all([x in self.split for x in ['variable', 'year']]):
                # split by variable and year
                self.split_variable_yr()

            elif 'year' in self.split:
                # split by year
                self.split_yr()

            elif 'variable' in self.split:
                #split by variable
                self.split_variable()
        except TypeError:
            self.outputfile = '{}.{}'.format(self.outputprefix, self.ext)
            self.getdata(self.variables, self.years, self.outputfile)

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

    def split_yr(self):
        """Fetch variable split by year."""
        # generate output filenames
        outputfiles = ["{}_{}_{}.{}".format(self.outputprefix,
                                            "-".join(self.variables),
                                            yr, self.ext)
                       for yr in self.years]
        variables = len(outputfiles) * [self.variables]
        if not self.threads:
            pool = Pool()
        else:
            pool = Pool(nodes=self.threads)
        pool.map(self.getdata, variables, self.years, outputfiles)

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

    def split_var_list(self, variables):
        """Split the given variables in 2D and 3D"""
        self.pressure_level_vars = []
        self.single_level_vars = []

        for v in variables:
            try:
                if v in plvars:
                    self.pressure_level_vars += [v]
                elif v in slvars:
                    self.single_level_vars += [v]
                else:
                     raise Exception('Invalid variable: {}'.v)

    def getdata(self, variables, years, outputfile):
        """Fetch variables using cds api call."""
        c = cdsapi.Client()
        # split variables into 2D and 3D vars
        self.split_var_list(variables)

        if 
            c.retrieve('reanalysis-era5-single-levels',
                       {'variable': self.single_level_vars,
                        'product_type': 'reanalysis',
                        'year': years,
                        'month': self.months,
                        'day': self.days,
                        'time': self.hours,
                        'format': self.outputformat},
                       outputfile)

            c.retrieve('reanalysis-era5-pressure-levels',
                       {'variable': plvariables,
                        'pressure_level': self.pressure_level_vars,
                        'product_type': 'reanalysis',
                        'year': years,
                        'month': self.months,
                        'day': self.days,
                        'time': self.hours,
                        'format': self.outputformat},
                       outputfile)
