"""Fetch ERA5 variables."""

import cdsapi
# from pathos.multiprocessing import ProcessPool as Pool
from pathos.threading import ThreadPool as Pool
import era5cli.inputref as ref
from era5cli.utils import format_hours
from era5cli.utils import zpad_days
from era5cli.utils import zpad_months


class Fetch:
    """Fetch ERA5 data using cdsapi."""

    def __init__(self, years: list, months: list, days: list,
                 hours: list, variables: list, outputformat: str,
                 outputprefix: str, period: str, ensemble: bool,
                 statistics=None, synoptic=None, pressurelevels=ref.plevels,
                 split=True, threads=None):
        """Initialization of Fetch class."""
        self.months = zpad_months(months)
        self.days = zpad_days(days)
        self.hours = format_hours(hours)
        self.pressurelevels = pressurelevels
        self.variables = variables
        self.outputformat = outputformat
        self.years = years
        self.outputprefix = outputprefix
        self.threads = threads
        self.split = split
        self.period = period
        self.ensemble = ensemble
        self.statistics = statistics # only for hourly data
        self.synoptic = synoptic # only for monthly data

        # define extension output filename
        self.extension()

    def fetch(self):
        """Split calls and fetch results."""
        if self.split:
            # split by variable and year
            self.split_variable_yr()
        else:
            # split by variable
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


    def product_type(self):
        # construct the product type name from the options
        producttype = ""

        if self.ensemble:
            producttype += "ensemble_members"
        elif not self.ensemble:
            producttype += "reanalysis"

        if self.period == "monthly":
            producttype = "monthly_averaged_" + producttype
            if self.synoptic:
                producttype += "_by_hour_of_day"
        elif self.period == "hourly":
            if self.ensemble and self.statistics:
                producttype = [
                    "ensemble_members",
                    "ensemble_mean",
                    "ensemble_spread",
                ]

        return producttype

    def build_request(self, variable):
        """Build the download request for the retrieve method of cdsapi."""
        name = "reanalysis-era5-"
        request = {'variable': variable,
                   'year': self.years,
                   'product_type': self.product_type(),
                   'month': self.months,
                   'day': self.days,
                   'time': self.hours,
                   'format': self.outputformat}

        if variable in ref.plvars:
            if all([l in ref.plevels for l in self.pressure_levels]):
                name += "pressure-levels-"
                request["pressure_level"] = self.pressure_levels
            else:
                raise Exception('''
                                Invalid pressure levels. Allowed values are: {}
                                '''.format(ref.plevels))
        elif variable in ref.slvars:
            name += "single-levels-"
        else:
            raise Exception('Invalid variable name: {}'.format(variable))

        if self.period == "monthly":
            name += "monthly-means"

        return(name,request)

    def getdata(self, outputfile: str):
        """Fetch variables using cds api call."""
        c = cdsapi.Client()
        name,request = self.build_request()
        c.retrieve(name, request, outputfile)

