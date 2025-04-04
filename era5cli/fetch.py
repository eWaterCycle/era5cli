"""Fetch ERA5 variables."""

import itertools
import logging
import os
import sys
import cdsapi
from pathos.threading import ThreadPool as Pool
import era5cli.inputref as ref
import era5cli.utils
from era5cli import key_management
from era5cli._request_size import TooLargeRequestError
from era5cli._request_size import request_too_large


class Fetch:
    """Fetch ERA5 data using cdsapi.

    Parameters
    ----------
        years: list(int)
            List of years to download data for.
        months: list(int)
            List of months to download data for (1-12).
        days: list(int), None
            List of days of the month to download data for (1-31).
        hours: list(int)
            List of time of day in hours to download data for (0-23).
            When downloading synoptic monthly data, this parameter is used
            to list the synoptic hours to download data for.
        variables: list(str)
            List of variable names to download data for. See the Copernicus
            Climate Data Store website for available variables.
        area: None, list(float)
            Coordinates in case extraction of a subregion is requested.
            Specified as [lat_max, lon_min, lat_min, lon_max]
            (counterclockwise coordinates, starting at the top),
            with longitude in the range -180, +180
            and latitude in the range -90, +90. For example:
            [90, -180, -90, 180]. Requests are rounded down to
            two decimals. By default, the entire available area
            will be returned.
        outputformat: str
            Output file type: 'netcdf' or 'grib'.
        outputprefix: str
            Prefix to be used for the output filename.
        period: str
            Execute the data fetch process for this data type:
            'hourly' or 'monthly'.
        ensemble: bool
            Whether to download high resolution realisation
            (HRES) or a reduced resolution ten member ensemble
            (EDA). If `True` the reduced resolution is fetched.
            `ensemble = True` is incompatible with `land = True`.
        statistics: None, bool
            When downloading hourly ensemble data, choose
            whether or not to download statistics (ensemble mean
            and ensemble spread).
        synoptic: None, bool
            Whether to get monthly averaged by hour of day
            (`synoptic = True`) or monthly means of daily means
            (`synoptic = False`).
        pressurelevels: None, list
            List of pressure level(s) to download 3D variables for.
            See the Copernicus Climate Data Store website for available
            pressure levels. For geopotential,
            `--levels surface` can be used to request data from
            the single level dataset (previously called orography).
        merge: bool
            Merge yearly output files (`merge = True`), or split
            output files into separate files for every year
            (`merge = False`).
        threads: None, int
            Number of parallel threads to use when downloading.
            Defaults to a single process.
        dryrun: bool
            Whether to print the cdsapi request to the screen,
            or make the request to start downloading the data.
            `dryrun = True` will print the request to stdout. By default,
            the data will be downloaded.
        land: bool
            Whether to download data from the ERA5-Land dataset.
            Note that the ERA5-Land dataset starts in 1981.
            `land = True` is incompatible with the use of
            `ensemble = True`.
        overwrite: bool
            Whether to overwrite existing files or not.
            Setting `overwrite = True` will make
            era5cli overwrite existing files. By default,
            you will be prompted if a file already exists, with
            the question if you want to overwrite it or not.
        dashed_vars: bool
            Whether to use dashed variable names in the output
            files, or the normal names ('temperature-of-snow-layer'
            instead of 'temperature_of_snow_layer').
    """

    def __init__(
        self,
        years: list,
        months: list,
        days: list,
        hours: list,
        variables: list,
        outputformat: str,
        outputprefix: str,
        period: str,
        ensemble: bool,
        area=None,
        statistics=None,
        synoptic=None,
        pressurelevels=None,
        splitmonths=False,
        merge=False,
        threads=None,
        land=False,
        overwrite=False,
        dashed_vars=False,
        dryrun=False,
    ):
        """Initialization of Fetch class."""
        self._get_login(dryrun=dryrun)  # Get login info from config file.

        self.months = era5cli.utils._zpad_months(months)
        """list(str): List of zero-padded strings of months
        (e.g. ['01', '02',..., '12'])."""
        if period == "monthly":
            self.days = None
        else:
            self.days = era5cli.utils._zpad_days(days)
            """list(str): List of zero-padded strings of days
            (e.g. ['01', '02',..., '31'])."""

        self.hours = era5cli.utils._format_hours(hours)
        """list(str): List of xx:00 formatted time strings
        (e.g. ['00:00', '01:00', ..., '23:00'])."""
        self.pressure_levels = pressurelevels
        """list(any): List of pressure levels (integer), or the indication
        'surface', requesting data only from a single-level dataset."""
        self.variables = variables
        """list(str): List of variables."""
        self.area = area
        """list(float): Coordinates specifying the subregion that will be
        extracted. Default is None for whole available area."""
        self.outputformat = outputformat
        """str: File format of output file."""
        self.years = years
        """list(int): List of years."""
        self.outputprefix = outputprefix
        """str: Prefix of output filename."""
        self.threads = threads
        """int: number of parallel threads to use for downloading."""
        self.splitmonths = splitmonths
        """bool: Split request per month, can avoid Too Large Request error."""
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
        self.land = land
        """bool: Whether to download from the ERA5-Land
        dataset."""
        self.overwrite = overwrite
        """bool: Whether to overwrite existing files."""
        self.dashed_vars = dashed_vars
        """bool: Whether to use dashed variable names in the output
        files, or the normal names."""

        if self.merge and self.splitmonths:
            self.splitmonths = False

        vars = list(self.variables)  # Use list() to avoid copying by reference
        if "geopotential" in vars and pressurelevels == ["surface"]:
            vars.remove("geopotential")
        if any([var in ref.PLVARS for var in vars]):
            self._check_levels()

        if self.period == "hourly" and request_too_large(self):
            raise TooLargeRequestError(
                "\n  Your request is too large for the CDS API."
                "\n  Consider splitting up your request in months, "
                "\n  by using '--splitmonths True'."
                "\n  For more info see 'era5cli hourly --help'."
            )

    def _get_login(self, dryrun=False):
        if dryrun:  # Don't check keys on dry run
            return None

        # First check if the config exists, and guide the user if it does not.
        key_management.check_era5cli_config()
        # Only then load the keys (as they should be there now).
        self.url, self.key = key_management.load_era5cli_config()

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

        if self.splitmonths:
            self._split_variable_yr_month()
        elif not self.merge:
            self._split_variable_yr()
        else:
            self._split_variable()

    def _extension(self):
        """Set filename extension."""
        if self.outputformat.lower() == "netcdf":
            self.ext = "nc"
        elif self.outputformat.lower() == "grib":
            self.ext = "grb"
        else:
            raise ValueError(f"Unknown outputformat: {self.outputformat}")

    def _process_areaname(self):
        (lat_max, lon_min, lat_min, lon_max) = [round(c) for c in self.area]

        def lon(x):
            return f"{x}E" if x >= 0 else f"{abs(x)}W"

        def lat(y):
            return f"{y}N" if y >= 0 else f"{abs(y)}S"

        name = f"_{lon(lon_min)}-{lon(lon_max)}_{lat(lat_min)}-{lat(lat_max)}"
        return name

    def _define_outputfilename(self, var, years, month=None):
        """Define output filename."""
        start, end = years[0], years[-1]

        prefix = f"{self.outputprefix}-land" if self.land else self.outputprefix

        yearblock = f"{start}-{end}" if start != end else f"{start}"

        varname = var.replace("_", "-") if self.dashed_vars else var

        fname = f"{prefix}_{varname}_{yearblock}"

        if month is not None:
            fname += f"-{month}"
        fname += f"_{self.period}"

        if self.area:
            fname += self._process_areaname()
        if self.ensemble:
            fname += "_ensemble"
        if self.statistics:
            fname += "_statistics"
        if self.synoptic:
            fname += "_synoptic"
        fname += f".{self.ext}"
        return fname

    def _split_variable(self):
        """Split by variable."""
        outputfiles = [
            self._define_outputfilename(var, self.years) for var in self.variables
        ]
        if not self.overwrite:
            era5cli.utils.assert_outputfiles_not_exist(outputfiles)

        years = len(outputfiles) * [self.years]

        pool = Pool(nodes=self.threads) if self.threads else Pool()
        pool.map(self._getdata, self.variables, years, outputfiles)

    def _split_variable_yr(self):
        """Fetch variable split by variable and year."""
        outputfiles = []
        variables = []
        for var in self.variables:
            outputfiles += [self._define_outputfilename(var, [yr]) for yr in self.years]
            variables += len(self.years) * [var]

        if not self.overwrite:
            era5cli.utils.assert_outputfiles_not_exist(outputfiles)

        years = len(self.variables) * self.years

        pool = Pool(nodes=self.threads) if self.threads else Pool()
        pool.map(self._getdata, variables, years, outputfiles)

    def _split_variable_yr_month(self):
        """Fetch variable split by variable, year, and month."""
        outputfiles = []
        variables = []
        years = []
        months = []

        for var, year, month in itertools.product(
            self.variables, self.years, self.months
        ):
            outputfiles += [self._define_outputfilename(var, [year, year], month)]
            variables += [var]
            years += [year]
            months += [month]

        if not self.overwrite:
            era5cli.utils.assert_outputfiles_not_exist(outputfiles)

        pool = Pool(nodes=self.threads) if self.threads else Pool()
        pool.map(self._getdata, variables, years, outputfiles, months)

    def _product_type(self):
        """Construct the product type name from the options."""
        assert not (
            self.land and self.ensemble
        ), "ERA5-Land does not contain Ensemble statistics."

        if self.period == "hourly" and self.ensemble and self.statistics:
            # The only configuration to return a list
            return [
                "ensemble_members",
                "ensemble_mean",
                "ensemble_spread",
            ]

        if self.land and self.period == "hourly":
            # The only configuration to return None
            return None

        # Default flow
        if self.ensemble:
            producttype = "ensemble_members"
        else:
            producttype = "reanalysis"

        if self.period == "hourly":
            return producttype

        producttype = "monthly_averaged_" + producttype
        if self.synoptic:
            producttype += "_by_hour_of_day"

        return producttype

    def _check_levels(self):
        """Retrieve pressure level info for request"""
        if not self.pressure_levels:
            raise ValueError(
                "Requested 3D variable(s), but no pressure levels specified."
                "Aborting."
            )
        if not all(level in ref.PLEVELS for level in self.pressure_levels):
            raise ValueError(
                f"Invalid pressure levels. Allowed values are: {ref.PLEVELS}"
            )

    def _check_variable(self, variable):
        """Check variable available and compatible with other inputs."""
        # if land then the variable must be in era5 land
        if self.land:
            if variable not in ref.ERA5_LAND_VARS:
                raise ValueError(
                    f"Variable {variable} is not available in ERA5-Land.\n"
                    f"Choose from {ref.ERA5_LAND_VARS}"
                )
        elif variable in ref.PLVARS + ref.SLVARS:
            if self.period == "monthly" and variable in ref.MISSING_MONTHLY_VARS:
                header = (
                    "There is no monthly data available for the "
                    "following variables:\n"
                )
                raise ValueError(
                    era5cli.utils.print_multicolumn(header, ref.MISSING_MONTHLY_VARS)
                )
        else:
            raise ValueError(f"Invalid variable name: {variable}")

    def _check_area(self):
        """Confirm that area parameters are correct."""
        (lat_max, lon_min, lat_min, lon_max) = self.area
        if not (
            -90 <= lat_max <= 90
            and -90 <= lat_min <= 90
            and -180 <= lon_min <= 180
            and -180 <= lon_max <= 180
            and lat_max > lat_min
            and lon_max != lon_min
        ):
            raise ValueError(
                "Provide coordinates as lat_max lon_min lat_min lon_max. "
                "Longitude must be in range -180,+180 and "
                "latitude must be in range -90,+90."
            )

    def _parse_area(self):
        """Parse area parameters to accepted coordinates."""
        self._check_area()
        area = [round(coord, ndigits=2) for coord in self.area]
        if self.area != area:
            print(f"NB: coordinates {self.area} rounded down to two decimals.\n")
        return area

    def _build_name(self, variable):
        """Build up name of dataset to use"""

        name = "reanalysis-era5"

        # report to user in case of ambiguous vars
        if (variable in ref.PLVARS) and (variable in ref.SLVARS):
            instruction_pressure = (
                "Getting variable from pressure level data. To get the "
                "surface variable instead, add `--levels surface` or "
                "`levels=['surface']` to the request.\n"
            )
            instruction_surface = (
                "Getting variable from surface level data. To get the "
                "pressure variable instead, omit `--levels surface` or "
                "`levels=['surface']` from the request.\n"
            )
            if self.pressure_levels == ["surface"]:
                instruction = instruction_surface
            else:
                instruction = instruction_pressure
            logging.warning(
                f"The variable name '{variable}' is ambiguous. {instruction}"
            )

        if self.land:
            name += "-land"
        elif self.pressure_levels == ["surface"]:
            name += "-single-levels"
        elif variable in ref.PLVARS:
            name += "-pressure-levels"
        elif variable in ref.SLVARS:
            name += "-single-levels"
        else:
            raise ValueError(f"Invalid variable name: {variable}")

        if self.period == "monthly":
            name += "-monthly-means"

        return name, variable

    def _build_request(self, variable, years, months=None):
        """Build the download request for the retrieve method of cdsapi."""
        self._check_variable(variable)

        name, variable = self._build_name(variable)

        request = {
            "variable": variable,
            "year": years,
            "month": self.months if months is None else months,
            "time": self.hours,
            "data_format": self.outputformat,
            "download_format": (
                "unarchived" if self.outputformat.lower() == "netcdf" else "zip"
            ),
        }

        if "pressure-levels" in name:
            request["pressure_level"] = self.pressure_levels

        if self.area:
            request["area"] = self._parse_area()

        product_type = self._product_type()
        if product_type is not None:
            request["product_type"] = product_type

        if self.period == "hourly":
            request["day"] = self.days

        return (name, request)

    def _exit(self):
        pass

    def _getdata(self, variables: list, years: list, outputfile: str, months=None):
        """Fetch variables using cds api call."""
        name, request = self._build_request(variables, years, months)
        if self.dryrun:
            print(name, request, outputfile)
        else:
            queueing_message = (
                os.linesep,
                "Download request is being queued at Copernicus.",
                os.linesep,
                "It can take some time before downloading starts, ",
                "please do not kill this process in the meantime.",
                os.linesep,
            )
            connection = cdsapi.Client(
                url=self.url,
                key=self.key,
                verify=True,
                progress=sys.stdin.isatty(),  # only show progress in interactive sesh.
            )
            print("".join(queueing_message))  # print queueing message
            connection.retrieve(name, request, outputfile)
            era5cli.utils.append_history(name, request, outputfile)
