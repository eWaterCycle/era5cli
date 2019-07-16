"""Fetch ERA5 variables."""

import os

import cdsapi
from pathos.threading import ThreadPool as Pool

import era5cli.inputref as ref
import era5cli.utils


class Fetch:
    """Fetch ERA5 data using cdsapi.

    Parameters
    ----------
        years: list(int)
            List of years to download data for.
        months: list(int)
            List of month to download data for (1-12).
        days: list(int), None
            List of days of month to download data for (1-31).
        hours: list(int)
            List of time in hours to download data for (0-23). When downloading
            synoptic monthly data, this parameter is used to list the synoptic
            hours to download data for.
        variables: list(str)
            List of variable names to download data for.
        outputformat: str
            Type of file to download: 'netcdf' or 'grib'.
        outputprefix: str
            Prefix to be used for the output filename.
        period: str
            Frequency of the data to be downloaded: 'hourly' or 'monthly'.
        ensemble: bool
            Whether to download high resolution realisation
            (HRES) or a reduced resolution ten member ensemble
            (EDA). If `True` the reduced resolution is fetched.
        statistics: None, bool
            When downloading hourly ensemble data, choose
            whether or not to download statistics (mean and
            spread).
        synoptic: None, bool
            Whether to get monthly averaged by hour of day
            (synoptic=True) or monthly means of daily means
            (synoptic=False).
        pressurelevels: None, list(int)
            List of pressure levels to download 3D variables for.
        merge: bool
            Merge yearly output files (merge=True), or split
            output files into separate files for every year
            (merge=False).
        threads: None, int
            Number of parallel calls to cdsapi. If `None` no
            parallel calls are done.
        dryrun: bool
            Indicating if files should be downloaded. By default
            files will be downloaded. For a dryrun the cdsapi request will
            be written to stdout.
    """

    def __init__(self, years: list, months: list, days: list,
                 hours: list, variables: list, outputformat: str,
                 outputprefix: str, period: str, ensemble: bool,
                 statistics=None, synoptic=None, pressurelevels=None,
                 merge=False, threads=None):
        """Initialization of Fetch class."""
        self.months = era5cli.utils._zpad_months(months)
        """list(str): List of zero-padded strings of months
        (e.g. ['01', '02',..., '12'])."""
        if period == 'monthly':
            self.days = None
        else:
            self.days = era5cli.utils._zpad_days(days)
            """list(str): List of zero-padded strings of days
            (e.g. ['01', '02',..., '12'])."""

        self.hours = era5cli.utils._format_hours(hours)
        """list(str): List of xx:00 formatted time strings
        (e.g. ['00:00', '01:00', ..., '23:00'])."""
        self.pressure_levels = pressurelevels
        """list(int): List of pressure levels."""
        self.variables = variables
        """list(str): List of variables."""
        self.outputformat = outputformat
        """str: File format of output file."""
        self.years = years
        """list(int): List of years."""
        self.outputprefix = outputprefix
        """str: Prefix of output filename."""
        self.threads = threads
        """int: number of parallel threads to use for downloading."""
        self.merge = merge
        """bool: Merge yearly output files if True."""
        self.period = period
        """str: Frequency of output data (monthly or daily)."""
        self.ensemble = ensemble
        """bool: Whether to download high resolution realisation
        (HRES) or a reduced resolution ten member ensemble
        (EDA). True downloads the reduced resolution
        ensemble."""
        self.statistics = statistics  # only for hourly data
        """bool: When downloading hourly ensemble data, choose
        whether or not to download statistics (mean and
        spread)."""
        self.synoptic = synoptic  # only for monthly data
        """bool: Whether to get monthly averaged by hour of day
        (synoptic=True) or monthly means of daily means
        (synoptic=False)."""

    def fetch(self, dryrun=False):
        """Split calls and fetch results.

        Parameters
        ----------
        dryrun: bool
            Boolean indicating if files should be downloaded. By default
            files will be downloaded. For a dryrun the cdsapi request will
            be written to stdout.
        """
        self.dryrun = dryrun
        # define extension output filename
        self._extension()
        # define fetch call depending on split argument
        if not self.merge:
            # split by variable and year
            self._split_variable_yr()
        else:
            # split by variable
            self._split_variable()

    def _extension(self):
        """Set filename extension."""
        if self.outputformat.lower() == 'netcdf':
            self.ext = "nc"
        elif self.outputformat.lower() == 'grib':
            self.ext = 'grb'
        else:
            raise ValueError('Unknown outputformat: {}'.format(
                self.outputformat))

    def _define_outputfilename(self, var, years):
        """Define output filename."""
        start_year = years[0]
        end_year = years[-1]
        if not end_year or (end_year == start_year):
            fname = ("{}_{}_{}_{}".format(
                self.outputprefix, var,
                start_year, self.period))
        else:
            fname = ("{}_{}_{}-{}_{}".format(
                self.outputprefix, var,
                start_year, end_year, self.period))
        if self.ensemble:
            fname += "_ensemble"
        if self.statistics:
            fname += "_statistics"
        if self.synoptic:
            fname += "_synoptic"
        fname += ".{}".format(self.ext)
        return fname

    def _split_variable(self):
        """Split by variable."""
        outputfiles = [self._define_outputfilename(var, self.years)
                       for var in self.variables]
        years = len(outputfiles) * [self.years]
        if not self.threads:
            pool = Pool()
        else:
            pool = Pool(nodes=self.threads)
        pool.map(self._getdata, self.variables, years, outputfiles)

    def _split_variable_yr(self):
        """Fetch variable split by variable and year."""
        outputfiles = []
        variables = []
        for var in self.variables:
            outputfiles += ([self._define_outputfilename(var, [yr])
                             for yr in self.years])
            variables += len(self.years) * [var]
        years = len(self.variables) * self.years
        if not self.threads:
            pool = Pool()
        else:
            pool = Pool(nodes=self.threads)
        pool.map(self._getdata, variables, years, outputfiles)

    def _product_type(self):
        """Construct the product type name from the options."""
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

    def _build_request(self, variable, years):
        """Build the download request for the retrieve method of cdsapi."""
        name = "reanalysis-era5-"
        request = {'variable': variable,
                   'year': years,
                   'product_type': self._product_type(),
                   'month': self.months,
                   'time': self.hours,
                   'format': self.outputformat}

        # variable is pressure level variable
        if variable in ref.PLVARS:
            try:
                if all([l in ref.PLEVELS for l in self.pressure_levels]):
                    name += "pressure-levels"
                    request["pressure_level"] = self.pressure_levels
                else:
                    raise ValueError(
                        "Invalid pressure levels. Allowed values are: {}"
                        .format(ref.PLEVELS))
            except TypeError:
                raise ValueError(
                    "Invalid pressure levels. Allowed values are: {}"
                    .format(ref.PLEVELS))
        # variable is single level variable
        elif variable in ref.SLVARS:
            name += "single-levels"
        # variable is unknown
        else:
            raise ValueError('Invalid variable name: {}'.format(variable))

        if self.period == "monthly":
            name += "-monthly-means"
            if variable in ref.MISSING_MONTHLY_VARS:
                header = ("There is no monthly data available for the "
                          "following variables:\n")
                raise ValueError(era5cli.utils._print_multicolumn(
                    header,
                    ref.MISSING_MONTHLY_VARS))
        elif self.period == "hourly":
            # Add day list to request if applicable
            if self.days:
                request["day"] = self.days

        return(name, request)

    def _exit(self):
        pass

    def _getdata(self, variables: list, years: list, outputfile: str):
        """Fetch variables using cds api call."""
        name, request = self._build_request(variables, years)
        if self.dryrun:
            print(name, request, outputfile)
        else:
            queueing_message = (
                os.linesep,
                "Download request is being queued at Copernicus.",
                os.linesep,
                "It can take some time before downloading starts, ",
                "please do not kill this process in the meantime.",
                os.linesep
                )
            connection = cdsapi.Client()
            print("".join(queueing_message))  # print queueing message
            connection.retrieve(name, request, outputfile)
            era5cli.utils._append_history(outputfile)
