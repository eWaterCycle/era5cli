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


def main():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command', dest='command')
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        "variables", type=str, nargs="+",
        help=textwrap.dedent('''
                             The variable to be downloaded. See the cds
                             website or the info argument for availabe
                             variables.
                             ''')
    )

    common.add_argument(
        "--years", type=str_seq,
        required=True,
        help=textwrap.dedent('''\
                             Year(s) for which the data should be downloaded.
                             ''')
    )

    common.add_argument(
        "--months", nargs="+",
        required=False, type=int,
        default=[str(m).zfill(2) for m in list(range(1, 13))],
        help=textwrap.dedent('''\
                             Months to download data for. Defaults to all
                             months.
                             ''')
    )

    common.add_argument(
        "--days", nargs="+",
        required=False, type=int,
        default=[str(d).zfill(2) for d in list(range(1, 32))],
        help=textwrap.dedent('''\
                             Days to download data for. Defaults to all days.
                             ''')
    )

    common.add_argument(
        "--hours", nargs="+",
        required=False, type=int,
        default=list(range(0, 24)),
        help=textwrap.dedent('''\
                             Time of day in hours to download data for.
                             Defaults to all hours.
                             ''')
    )

    common.add_argument(
        "--levels", nargs="+", type=int,
        required=False,
        help=textwrap.dedent('''\
                             Pressure levels to download for three dimensional
                             data. Default is all available levels. See the
                             cds website or the info argument for availabe
                             variables.
                             ''')
    )

    common.add_argument(
        "--outputprefix", type=str, default='era5',
        help=textwrap.dedent('''\
                             Prefix of output filename. Default prefix is
                             era5.
                             ''')
    )

    common.add_argument(
        "--format", type=str,
        default="netcdf", choices=["netcdf", "grib"],
        help="Output file type. Defaults to 'netcdf'."
    )

    common.add_argument(
        "--split", type=bool,
        default=True, required=False,
        help=textwrap.dedent('''
                             Split output by years. Default is True.
                             ''')
    )

    common.add_argument(
        "--threads", type=int, choices=range(1, 7),
        required=False, default=None,
        help=textwrap.dedent('''\
                             Number of parallel threads to use when downloading
                             using split. Default is a single process.
                             ''')
    )

    hourly = subparsers.add_parser(
        'fetchhourly', parents=[common],
        description='Execute the data fetch process.',
        formatter_class=argparse.RawTextHelpFormatter)

    hourly.add_argument(
        "--product", type=str,
        required=True, choices=[
            'ensemble_mean',
            'ensemble_members',
            'ensemble_spread',
            'reanalysis'
        ],
        help=textwrap.dedent(
            "The product type to be downloaded for hourly data."
        )
    )

    monthly = subparsers.add_parser(
        'fetchmonthly', parents=[common],
        description='Execute the data fetch process.',
        formatter_class=argparse.RawTextHelpFormatter)

    monthly.add_argument(
        "--ensemble", type=bool, required=True,
        help=textwrap.dedent('''
                             Whether to download high resolution realisation
                             (HRES) or a reduced resolution ten member ensemble
                             (EDA)
                             ''')
    )

    monthly.add_argument(
        "--synaptic", type=bool, required=True,
        help=textwrap.dedent('''
                             Whether to download high resolution realisation
                             (HRES) or a reduced resolution ten member ensemble
                             (EDA)
                             ''')
    )

    info = subparsers.add_parser(
        'info',
        description='Show information on available variables and levels.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    info.add_argument(
        "type", type=str, choices=ref.refdict,
        help=textwrap.dedent('''\
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
        years = args.years
        outputprefix = args.outputprefix
        # Fetch the data
        era5 = Fetch(years, months, days, hours, variables, outputformat,
                     outputprefix, split, threads)
        era5.fetch()


if __name__ == "__main__":
    main()
