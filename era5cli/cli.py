#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
import sys

from datetime import datetime

import era5cli.inputref as ref
import era5cli.info as einfo
import era5cli.fetch as efetch


def _level_parse(level):
    """Parse levels as integers, or the string 'surface'"""
    if level == "surface":
        return str(level)
    return int(level)


def _build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="sub-command", dest="command")
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        "--variables",
        type=str,
        required=True,
        nargs="+",
        help=textwrap.dedent(
            """
            The variables to download data for. This can be a
            single variable, or multiple. See the Copernicus
            Climate Data Store website or run
            `era5cli info -h` for available variables.

            """
        ),
    )

    common.add_argument(
        "--startyear",
        type=int,
        required=True,
        help=textwrap.dedent(
            """
            Single year or first year of range for which
            data should be downloaded.
            Every year will be downloaded in a separate file
            by default. Set `--split false` to change this

            """
        ),
    )

    common.add_argument(
        "--endyear",
        type=int,
        required=False,
        default=None,
        help=textwrap.dedent(
            """
            Last year of range for which data should be
            downloaded.
            If only a single year is needed, only
            `--startyear` needs to be specified.
            Every year will be downloaded in a separate file
            by default. Set `--split false` to change this

            """
        ),
    )

    common.add_argument(
        "--levels",
        nargs="+",
        type=_level_parse,
        required=False,
        default=ref.PLEVELS,
        help=textwrap.dedent(
            """
            Pressure level(s) to download 3D variables for.
            Default is all available levels. See the Copernicus
            Climate Data Store website or run `era5cli info -h`
            for available pressure levels. For geopotential,
            `--levels surface` can be used to request data from
            the single level dataset (previously called
            orography)

            """
        ),
    )

    common.add_argument(
        "--outputprefix",
        type=str,
        default="era5",
        help=textwrap.dedent(
            """
            Prefix to be used for the output filename.
            Default prefix is `era5`

            """
        ),
    )

    common.add_argument(
        "--format",
        type=str,
        default="netcdf",
        choices=["netcdf", "grib"],
        help=textwrap.dedent(
            """
            Output file type. Defaults to `netcdf`

            """
        ),
    )

    common.add_argument(
        "--merge",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Merge yearly output files.
            Default is split output files into separate files
            for every year

            """
        ),
    )

    common.add_argument(
        "--threads",
        type=int,
        choices=range(1, 7),
        required=False,
        default=None,
        help=textwrap.dedent(
            """
            Number of parallel threads to use when
            downloading. Defaults to a single process

            """
        ),
    )

    common.add_argument(
        "--ensemble",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download high resolution realisation
            (HRES) or a reduced resolution ten member ensemble
            (EDA). Providing the `--ensemble` argument
            downloads the reduced resolution ensemble.
            `--ensemble` is incompatible with `--land`

            """
        ),
    )

    common.add_argument(
        "--dryrun",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to print the cdsapi request to the screen,
            or make the request to start downloading the data.
            Providing the `--dryrun` argument will print the
            request to stdout. By default, the data will be
            downloaded

            """
        ),
    )

    common.add_argument(
        "--prelimbe",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download the preliminary back extension
            (1950-1978). Note that when `--prelimbe` is used,
            `--startyear` and `--endyear` should be set
            between 1950 and 1978. Please, be aware that
            ERA5 data is available from 1959.
            `--prelimbe` is incompatible with `--land`

            """
        ),
    )

    common.add_argument(
        "--land",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download data from the ERA5-Land
            dataset. Note that the ERA5-Land dataset starts in
            1950.
            `--land` is incompatible with the use of
            `--prelimbe` and `--ensemble`

            """
        ),
    )

    common.add_argument(
        "--area",
        nargs=4,
        type=float,
        metavar=("LAT_MAX", "LON_MIN", "LAT_MIN", "LON_MAX"),
        required=False,
        help=textwrap.dedent(
            """
            Coordinates in case extraction of a subregion is
            requested.
            Specified as `LAT_MAX LON_MIN LAT_MIN LON_MAX`
            (counterclockwise coordinates, starting at the top)
            with longitude in the range -180, +180
            and latitude in the range -90, +90. For example:
            `--area 90 -180 -90 180`. Requests are rounded down
            to two decimals. By default, the entire
            available area will be returned

            """
        ),
    )

    mnth = argparse.ArgumentParser(add_help=False)

    mnth.add_argument(
        "--months",
        nargs="+",
        required=False,
        type=int,
        default=list(range(1, 13)),
        help=textwrap.dedent(
            """
            Month(s) to download data for. Defaults to all
            months. For every year, only these
            months will be downloaded

            """
        ),
    )

    day = argparse.ArgumentParser(add_help=False)

    day.add_argument(
        "--days",
        nargs="+",
        required=False,
        type=int,
        default=list(range(1, 32)),
        help=textwrap.dedent(
            """
            Day(s) to download data for. Defaults to all days.
            For every year, only these days will
            be downloaded

            """
        ),
    )

    hour = argparse.ArgumentParser(add_help=False)

    hour.add_argument(
        "--hours",
        nargs="+",
        required=False,
        type=int,
        default=list(range(0, 24)),
        help=textwrap.dedent(
            """
            Time of day in hours to download data for.
            Defaults to all hours. For every year,
            only these hours will be downloaded

            """
        ),
    )

    hourly = subparsers.add_parser(
        "hourly",
        parents=[common, mnth, day, hour],
        description="Execute the data fetch process for hourly data.",
        prog=textwrap.dedent(
            """
            Use `era5cli hourly --help` for more information

            """
        ),
        help=textwrap.dedent(
            """
            Execute the data fetch process for hourly data.
            Use `era5cli hourly --help` for more information

            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    hourly.add_argument(
        "--statistics",
        action="store_true",
        help=textwrap.dedent(
            """
            When downloading hourly ensemble data, provide
            the `--statistics` argument to download statistics
            (ensemble mean and ensemble spread)

            """
        ),
    )

    monthly = subparsers.add_parser(
        "monthly",
        parents=[common, mnth],
        description="Execute the data fetch process for monthly data.",
        prog=textwrap.dedent(
            """
            Use `era5cli monthly --help` for more information

            """
        ),
        help=textwrap.dedent(
            """
            Execute the data fetch process for monthly data.
            Use `era5cli monthly --help` for more information

            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    monthly.add_argument(
        "--synoptic",
        type=int,
        default=False,
        nargs="*",
        help=textwrap.dedent(
            """
            Time of day in hours to get the synoptic means
            (monthly averaged by hour of day) for. For example
            `--synoptic 0 4 5 6 23`. Give empty option
            `--synoptic` to download all hours (0-23).
            The option defaults to `None` in which case the
            monthly average of daily means is chosen

            """
        ),
    )

    info = subparsers.add_parser(
        "info",
        description="Show information on available variables and levels.",
        prog=textwrap.dedent(
            """
            Use `era5cli info --help` for more information

            """
        ),
        help=textwrap.dedent(
            """
            Show information on available variables or levels.
            Use `era5cli info --help` for more information

            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    info.add_argument(
        "name",
        type=str,
        help=textwrap.dedent(
            """
            Enter list name to print info list: \n
            `levels` for all available pressure levels \n
            `2Dvars` for all available single level or 2D
            variables \n
            `3Dvars` for all available 3D variables \n
            `land` for all available variables in
            ERA5-land \n
            Enter variable name (e.g. `total_precipitation`)
            or pressure level (e.g. `825`) to show if the
            variable or level is available, and in which list

            """
        ),
    )

    return parser


def _parse_args(args):
    """Parse command line arguments."""
    parser = _build_parser()
    return parser.parse_args(args)


def _run_info(args):
    # List dataset information
    era5info = einfo.Info(args.name)
    if era5info.infotype == "list":
        era5info.list()
        return True
    era5info.vars()
    return True


def _construct_year_list(args):
    if not args.endyear:
        endyear = args.startyear
    else:
        endyear = args.endyear

    # check whether correct years have been entered
    for year in (args.startyear, endyear):
        if args.prelimbe:
            assert 1950 <= year <= 1978, "year should be between 1950 and 1978"
        elif args.land:
            assert (
                1950 <= year <= datetime.now().year
            ), "for ERA5-Land, year should be between 1950 and present"
        else:
            assert (
                1959 <= year <= datetime.now().year
            ), "year should be between 1959 and present"

    assert endyear >= args.startyear, "endyear should be >= startyear or None"

    return list(range(args.startyear, endyear + 1))


def _set_period_args(args):
    # set subroutine specific arguments for monthly and hourly fetch
    if args.command == "monthly":
        statistics = None
        days = None
        if args.synoptic is False:
            synoptic = None
            hours = [0]
        elif len(args.synoptic) == 0:
            synoptic = True
            hours = range(24)
        else:
            synoptic = True
            hours = args.synoptic
    elif args.command == "hourly":
        synoptic = None
        statistics = args.statistics
        if statistics:
            assert args.ensemble, (
                "Statistics can only be computed over an ensemble, "
                "add --ensemble or remove --statistics."
            )
        days = args.days
        hours = args.hours
    else:
        raise AttributeError(f'The command "{args.command}" is not valid.')
    return synoptic, statistics, days, hours


def _execute(args):
    """Call to ERA-5 cli library."""
    # the info subroutine
    if args.command == "info":
        return _run_info(args)

    # the fetching subroutines
    years = _construct_year_list(args)
    synoptic, statistics, days, hours = _set_period_args(args)
    # try to build and send download request
    era5 = efetch.Fetch(
        years,
        months=args.months,
        days=days,
        hours=hours,
        variables=args.variables,
        area=args.area,
        outputformat=args.format,
        outputprefix=args.outputprefix,
        period=args.command,
        ensemble=args.ensemble,
        synoptic=synoptic,
        statistics=statistics,
        pressurelevels=args.levels,
        threads=args.threads,
        merge=args.merge,
        prelimbe=args.prelimbe,
        land=args.land,
    )
    era5.fetch(dryrun=args.dryrun)
    return True


def main(argv=None):
    """Main."""
    # get arguments
    if argv is None:
        argv = sys.argv
    args = _parse_args(argv[1:])
    _execute(args)


if __name__ == "__main__":
    main()
