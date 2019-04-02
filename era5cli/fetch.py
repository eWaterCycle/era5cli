"""Fetch ERA5 variables."""

import cdsapi
# from pathos.multiprocessing import ProcessPool as Pool
from pathos.threading import ThreadPool as Pool
import os


class Fetch:
    """Fetch ERA5 data using cdsapi."""

    def __init__(self, years, months, days, hours, variables, outputformat,
                 outputfile, split=None, threads=None):
        """Initialization of Fetch class."""
        self.months = months
        self.days = days
        self.hours = hours
        self.variables = variables
        self.outputformat = outputformat
        self.years = years
        self.outputfile = outputfile
        self.threads = threads

        if (split == 'year'):
            self.split_yr()
        elif not split:
            self.fetch(self.years, self.outputfile)

    def split_yr(self):
        """Fetch variable split by year."""
        (fname, ext) = os.path.splitext(self.outputfile)
        # generate output filenames
        outputfiles = ["{}_{}{}".format(fname, yr, ext) for yr in self.years]
        if not self.threads:
            pool = Pool()
        else:
            if (self.threads > len(self.years)):
                self.threads = len(self.years)
            pool = Pool(nodes=self.threads)
        pool.map(self.fetch, self.years, outputfiles)

    def fetch(self, years, outputfile):
        """Fetch variables using cds api call."""
        c = cdsapi.Client()
        c.retrieve('reanalysis-era5-single-levels',
                   {'variable': self.variables,
                    'product_type': 'reanalysis',
                    'year': self.years,
                    'month': self.months,
                    'day': self.days,
                    'time': self.hours,
                    'format': self.outputformat},
                   self.outputfile)
