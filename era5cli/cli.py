#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
from era5cli.fetch import Fetch
import era5cli.inputref as ref
from era5cli.info import Info


def str_seq(intseq):
    """Validate input argument and return a list of ints."""
    try:
        return [int(intseq)]
    except ValueError:
        return seq_to_list(intseq)


def seq_to_list(sequence):
    """Return a list from a sequence."""
    (first, last) = sequence.split('/')
    return list(range(int(first), int(last) + 1))


def str2bool(v):
    """Return boolean based on input string."""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command', dest='command')
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        "--variables", type=str, nargs="+",
        help=textwrap.dedent('''
                             The variable to be downloaded. See the cds
                             website or the info argument for availabe
                             variables.
                             ''')
    )

    common.add_argument(
        "--startyear", type=int,
        required=True,
        help=textwrap.dedent('''
                             Single year or first year of range for which
                             data should be downloaded.
                             ''')
    )

    common.add_argument(
        "--endyear", type=int,
        required=False, default=None,
        help=textwrap.dedent('''
                             Last year of range for which  data should be
                             downloaded. If only a single year is needed, only
                             --startyear needs to be specified.
                             ''')
    )

    common.add_argument(
        "--months", nargs="+",
        required=False, type=int,
        default=[str(m).zfill(2) for m in list(range(1, 13))],
        help=textwrap.dedent('''
                             Months to download data for. Defaults to all
                             months.
                             ''')
    )

    common.add_argument(
        "--days", nargs="+",
        required=False, type=int,
        default=[str(d).zfill(2) for d in list(range(1, 32))],
        help=textwrap.dedent('''
                             Days to download data for. Defaults to all days.
                             ''')
    )

    common.add_argument(
        "--hours", nargs="+",
        required=False, type=int,
        default=list(range(0, 24)),
        help=textwrap.dedent('''
                             Time of day in hours to download data for.
                             Defaults to all hours.
                             ''')
    )

    common.add_argument(
        "--levels", nargs="+", type=int,
        required=False,
        help=textwrap.dedent('''
                             Pressure levels to download for three dimensional
                             data. Default is all available levels. See the
                             cds website or the info argument for availabe
                             variables.
                             ''')
    )

    common.add_argument(
        "--outputprefix", type=str, default='era5',
        help=textwrap.dedent('''
                             Prefix of output filename. Default prefix is
                             era5.
                             ''')
    )

    common.add_argument(
        "--format", type=str, default="netcdf", choices=["netcdf", "grib"],
        help="Output file type. Defaults to 'netcdf'."
    )

    common.add_argument(
        "--split", type=str2bool, default=True, required=False,
        help=textwrap.dedent('''
                             Split output by years. Default is True.
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
        "--ensemble", type=str2bool, required=True,
        help=textwrap.dedent('''
                             Whether to download high resolution realisation
                             (HRES) or a reduced resolution ten member ensemble
                             (EDA). True downloads the reduced resolution
                             ensemble.
                             ''')
    )

    hourly = subparsers.add_parser(
        'fetchhourly', parents=[common],
        description='Execute the data fetch process.',
        formatter_class=argparse.RawTextHelpFormatter)

    hourly.add_argument(
        "--statistics", type=str2bool, required=True,
        help=textwrap.dedent('''
                             When downloading hourly ensemble data, choose
                             whether or not to download statistics (mean and
                             spread).
                             ''')
    )

    monthly = subparsers.add_parser(
        'fetchmonthly', parents=[common],
        description='Execute the data fetch process.',
        formatter_class=argparse.RawTextHelpFormatter)

    monthly.add_argument(
        "--synoptic", type=str2bool, required=True,
        help=textwrap.dedent('''
                             Whether to get monthly averaged by hour of day
                             (synoptic=True) or monthly means of daily means
                             (synoptic=False).
                             ''')
    )

    info = subparsers.add_parser(
        'info',
        description='Show information on available variables and levels.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    info.add_argument(
        "type", type=str, choices=ref.refdict,
        help=textwrap.dedent('''
                             Print lists of available variables or pressure
                             levels.
                           ''')
    )

    args = parser.parse_args()
    # input arguments
    try:
        infotype = args.type
        # List dataset information
        era5info = Info(infotype)
        era5info.list()

    except AttributeError:
        variables = args.variables
        months = args.months
        days = args.days
        hours = args.hours
        split = args.split
        outputformat = args.format
        threads = args.threads
        levels = args.levels
        outputprefix = args.outputprefix
        ensemble = args.ensemble
        period = None
        startyear = args.startyear
        endyear = args.endyear
        if not endyear:
            years = [startyear]
        else:
            assert (endyear >= endyear), (
                'endyear should be >= startyear or None')
            years = list(range(startyear, endyear + 1))

        try:
            statistics = args.statistics
            period = "monthly"
            era5 = Fetch(years,
                         months=months,
                         days=days,
                         hours=hours,
                         variables=variables,
                         outputformat=outputformat,
                         outputprefix=outputprefix,
                         period=period,
                         ensemble=ensemble,
                         statistics=statistics,
                         pressurelevels=levels,
                         threads=threads,
                         split=split)
            era5.fetch()
        except AttributeError:
            pass

        try:
            synoptic = args.synoptic
            period = "hourly"
            era5 = Fetch(years=years,
                         months=months,
                         days=days,
                         hours=hours,
                         variables=variables,
                         outputformat=outputformat,
                         outputprefix=outputprefix,
                         period=period,
                         ensemble=ensemble,
                         synoptic=synoptic,
                         pressurelevels=levels,
                         threads=threads,
                         split=split)
            era5.fetch()
        except AttributeError:
            pass


if __name__ == "__main__":
    main()
