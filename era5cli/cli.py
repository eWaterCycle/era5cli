#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
import sys
from era5cli.fetch import Fetch
from era5cli.info import Info


def _str2bool(v):
    """Return boolean based on input string."""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def _parse_args(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command', dest='command')
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        "--variables", type=str, nargs="+",
        help=textwrap.dedent('''\
                             The variables to be downloaded, can be a single
                             or multiple variables. See the cds
                             website or run "era5cli info -h" for available
                             variables.

                             ''')
    )

    common.add_argument(
        "--startyear", type=int,
        required=True,
        help=textwrap.dedent('''\
                             Single year or first year of range for which
                             data should be downloaded.
                             Every year will be downloaded in a seperate file
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
                             Every year will be downloaded in a seperate file
                             by default. Set "--split false" to change this.

                             ''')
    )

    common.add_argument(
        "--months", nargs="+",
        required=False, type=int,
        default=list(range(1, 13)),
        help=textwrap.dedent('''\
                             Month(s) to download data for. Defaults to all
                             months. For every year in "--years" only these
                             months will be downloaded.

                             ''')
    )

    common.add_argument(
        "--days", nargs="+",
        required=False, type=int,
        default=list(range(1, 32)),
        help=textwrap.dedent('''\
                             Day(s) to download data for. Defaults to all days.
                             For every year in "--years" only these days will
                             be downloaded.

                             ''')
    )

    common.add_argument(
        "--hours", nargs="+",
        required=False, type=int,
        default=list(range(0, 24)),
        help=textwrap.dedent('''\
                             Time of day in hours to download data for.
                             Defaults to all hours. For every year in
                             "--years" only these hours will be downloaded.

                             ''')
    )

    common.add_argument(
        "--levels", nargs="+", type=int,
        required=False,
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
        "--split", type=_str2bool, default=True,
        help=textwrap.dedent('''\
                             Split output by years, producing a seperate file
                             for every year in the "--years" argument. Default
                             is True.

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
        "--ensemble", type=_str2bool, default=False,
        help=textwrap.dedent('''\
                             Whether to download high resolution realisation
                             (HRES) or a reduced resolution ten member ensemble
                             (EDA). "--ensemble True" downloads the reduced
                             resolution ensemble.

                             ''')
    )

    hourly = subparsers.add_parser(
        'hourly', parents=[common],
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
        "--statistics", type=_str2bool, default=False,
        help=textwrap.dedent('''\
                             When downloading hourly ensemble data, set
                             "--statistics True" to download statistics
                             (ensemble mean and ensemble spread). Default is
                             False.

                             ''')
    )

    monthly = subparsers.add_parser(
        'monthly', parents=[common],
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
        "--synoptic", type=_str2bool, default=False,
        help=textwrap.dedent('''\
                             Set "--synoptic True" to get monthly averaged
                             by hour of day or set "--synoptic False" to get
                             monthly means of daily means. Default is False.

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
                             "2dvars" for all available single level or 2D
                             variables \n
                             "3dvars" for all available 3D variables \n
                             Enter variable name (e.g. "total_precipitation")
                             or pressure level (e.g. "825") to show if the
                             variable or level is available and in which list.

                             ''')
    )

    return parser.parse_args(args)


def main():
    """Main."""
    # get arguments
    args = _parse_args(sys.argv[1:])
    print(args)

    # the info subroutine
    if args.command == "info":
        # List dataset information
        era5info = Info(args.name)
        if era5info.infotype == "list":
            era5info.list()
        else:
            era5info.vars()

    # the fetching subroutines
    else:
        # make list of years to be downloaded
        if not args.endyear:
            years = [args.startyear]
        else:
            assert (args.endyear >= args.endyear), (
                'endyear should be >= startyear or None')
            years = list(range(args.startyear, args.endyear + 1))

        # set subroutine specific arguments for monthly and hourly fetch
        if args.command == "monthly":
            synoptic = args.synoptic
            statistics = None
        elif args.command == "hourly":
            statistics = args.statistics
            synoptic = None
        else:
            raise AttributeError(
                'The command "{}" is not valid.'.format(args.command)
            )

        # try to build and send download request
        try:
            era5 = Fetch(years,
                         months=args.months,
                         days=args.days,
                         hours=args.hours,
                         variables=args.variables,
                         outputformat=args.format,
                         outputprefix=args.outputprefix,
                         period=args.command,
                         ensemble=args.ensemble,
                         synoptic=synoptic,
                         statistics=statistics,
                         pressurelevels=args.levels,
                         threads=args.threads,
                         split=args.split)
            era5.fetch()
        except:
            raise Exception('Data could not be downloaded.')


if __name__ == "__main__":
    main()
