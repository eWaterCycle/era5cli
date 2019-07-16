#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
import sys

import era5cli.inputref as ref
import era5cli.info as einfo
import era5cli.fetch as efetch


def _build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command', dest='command')
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        "--variables", type=str, required=True, nargs="+",
        help=textwrap.dedent('''\
                             The variables to be downloaded, can be a single
                             or multiple variables. See the Copernicus Climate
                             Data Store website or run "era5cli info -h" for
                             available variables.

                             ''')
    )

    common.add_argument(
        "--startyear", type=int,
        required=True,
        help=textwrap.dedent('''\
                             Single year or first year of range for which
                             data should be downloaded.
                             Every year will be downloaded in a separate file
                             by default. Set "--split false" to change this.

                             ''')
    )

    common.add_argument(
        "--endyear", type=int,
        required=False, default=None,
        help=textwrap.dedent('''\
                             Last year of range for which  data should be
                             downloaded. If only a single year is needed, only
                             "--startyear" needs to be specified.
                             Every year will be downloaded in a separate file
                             by default. Set "--split false" to change this.

                             ''')
    )

    common.add_argument(
        "--levels", nargs="+", type=int,
        required=False, default=ref.PLEVELS,
        help=textwrap.dedent('''\
                             Pressure level(s) to download for three
                             dimensional data. Default is all available
                             levels. See the cds website or run "era5cli info
                             -h" for available pressure levels.

                             ''')
    )

    common.add_argument(
        "--outputprefix", type=str, default='era5',
        help=textwrap.dedent('''\
                             Prefix of output filename. Default prefix is
                             "era5".

                             ''')
    )

    common.add_argument(
        "--format", type=str, default="netcdf", choices=["netcdf", "grib"],
        help=textwrap.dedent('''\
                             Output file type. Defaults to 'netcdf'."

                             ''')
    )

    common.add_argument(
        "--merge", action="store_true", default=False,
        help=textwrap.dedent('''\
                             Merge yearly output files.
                             Default is split output files into separate files
                             for every year.

                             ''')
    )

    common.add_argument(
        "--threads", type=int, choices=range(1, 7),
        required=False, default=None,
        help=textwrap.dedent('''\
                             Number of parallel threads to use when
                             downloading. Default is a single process.

                             ''')
    )

    common.add_argument(
        "--ensemble", action="store_true", default=False,
        help=textwrap.dedent('''\
                             Whether to download high resolution realisation
                             (HRES) or a reduced resolution ten member ensemble
                             (EDA). Providing the "--ensemble" argument
                             downloads the reduced resolution ensemble.

                             ''')
    )

    common.add_argument(
        "--dryrun", action="store_true", default=False,
        help=textwrap.dedent('''\
                             Whether to start downloading the request or just
                             print information on the chosen parameters and
                             output file names. Providing the "--dryrun"
                             argument will print the information to stdout.

                             ''')
    )

    mnth = argparse.ArgumentParser(add_help=False)

    mnth.add_argument(
        "--months", nargs="+",
        required=False, type=int,
        default=list(range(1, 13)),
        help=textwrap.dedent('''\
                             Month(s) to download data for. Defaults to all
                             months. For every year, only these
                             months will be downloaded.

                             ''')
    )

    day = argparse.ArgumentParser(add_help=False)

    day.add_argument(
        "--days", nargs="+",
        required=False, type=int,
        default=list(range(1, 32)),
        help=textwrap.dedent('''\
                             Day(s) to download data for. Defaults to all days.
                             For every year, only these days will
                             be downloaded.

                             ''')
    )

    hour = argparse.ArgumentParser(add_help=False)

    hour.add_argument(
        "--hours", nargs="+",
        required=False, type=int,
        default=list(range(0, 24)),
        help=textwrap.dedent('''\
                             Time of day in hours to download data for.
                             Defaults to all hours. For every year,
                             only these hours will be downloaded.

                             ''')
    )

    hourly = subparsers.add_parser(
        'hourly', parents=[common, mnth, day, hour],
        description='Execute the data fetch process for hourly data.',
        prog=textwrap.dedent('''\
                             Use "era5cli hourly --help" for more information.

                             '''),
        help=textwrap.dedent('''\
                             Execute the data fetch process for hourly data.
                             Use "era5cli hourly --help" for more information.

                             '''),
        formatter_class=argparse.RawTextHelpFormatter)

    hourly.add_argument(
        "--statistics", action="store_true",
        help=textwrap.dedent('''\
                             When downloading hourly ensemble data, provide
                             the "--statistics" argument to download statistics
                             (ensemble mean and ensemble spread).

                             ''')
    )

    monthly = subparsers.add_parser(
        'monthly', parents=[common, mnth],
        description='Execute the data fetch process for monthly data.',
        prog=textwrap.dedent('''\
                             Use "era5cli monthly --help" for more information.

                             '''),
        help=textwrap.dedent('''\
                             Execute the data fetch process for monthly data.
                             Use "era5cli monthly --help" for more information.

                             '''),
        formatter_class=argparse.RawTextHelpFormatter
    )

    monthly.add_argument(
        "--synoptic", type=int, default=False, nargs="*",
        help=textwrap.dedent('''\
                             Time of day in hours to get the synoptic means
                             (monthly averaged by hour of day) for. For example
                             "--synoptic 0 4 5 6 23". Give empty option
                             "--synoptic" to download all hours (0-23).
                             The option defaults to "None" in which case the
                             monthly average of daily means is chosen.

                             ''')
    )

    info = subparsers.add_parser(
        'info',
        description='Show information on available variables and levels.',
        prog=textwrap.dedent('''\
                             Use "era5cli info --help" for more information.

                             '''),
        help=textwrap.dedent('''\
                             Show information on available variables or levels.
                             Use "era5cli info --help" for more information.

                             '''),
        formatter_class=argparse.RawTextHelpFormatter
    )

    info.add_argument(
        "name", type=str,
        help=textwrap.dedent('''\
                             Enter list name to print info list: \n
                             "levels" for all available pressure levels \n
                             "2Dvars" for all available single level or 2D
                             variables \n
                             "3Dvars" for all available 3D variables \n
                             Enter variable name (e.g. "total_precipitation")
                             or pressure level (e.g. "825") to show if the
                             variable or level is available and in which list.

                             ''')
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
    else:
        era5info.vars()
        return True


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
            hours = range(0, 24)
        else:
            synoptic = True
            hours = args.synoptic
    elif args.command == "hourly":
        synoptic = None
        statistics = args.statistics
        days = args.days
        hours = args.hours
    else:
        raise AttributeError(
            'The command "{}" is not valid.'.format(args.command)
        )
    return synoptic, statistics, days, hours


def _execute(args):
    """Call to ERA-5 cli library."""
    # the info subroutine
    if args.command == "info":
        _run_info(args)

    # the fetching subroutines
    else:
        # make list of years to be downloaded
        if not args.endyear:
            years = [args.startyear]
        else:
            assert (args.endyear >= args.startyear), (
                'endyear should be >= startyear or None')
            years = list(range(args.startyear, args.endyear + 1))

        synoptic, statistics, days, hours = _set_period_args(args)
        # try to build and send download request
        era5 = efetch.Fetch(years,
                            months=args.months,
                            days=days,
                            hours=hours,
                            variables=args.variables,
                            outputformat=args.format,
                            outputprefix=args.outputprefix,
                            period=args.command,
                            ensemble=args.ensemble,
                            synoptic=synoptic,
                            statistics=statistics,
                            pressurelevels=args.levels,
                            threads=args.threads,
                            merge=args.merge)
        era5.fetch(dryrun=args.dryrun)
        return True


def main():
    """Main."""
    # get arguments
    args = _parse_args(sys.argv[1:])
    _execute(args)


if __name__ == "__main__":
    main()
