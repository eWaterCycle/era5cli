#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
import sys
from era5cli.fetch import Fetch
import era5cli.inputref as ref


usage = """Usage:

    --years <years> --variable <variable>

    Examples:

    runoff for the year 2018
    >>> era5cli --years 2018 --variable runoff

    runoff for 2017 and 2018
    >>> era5cli --years 2017,2018 --variable runoff


""".format(__file__)


def zpadlist(intstr, type, minval, maxval):
    """Return zero padded string and perform input checks."""
    try:
        if (int(intstr) >= minval and int(intstr) <= maxval):
            pass
        else:
            print("Invalid {} argument: {}".format(type, intstr))
            sys.exit()
    except TypeError:
        print("Invalid {} argument: {}".format(type, intstr))
        sys.exit()
    return str(intstr.zfill(2))


def zpad_days(intstr):
    """Return zero padded string."""
    return zpadlist(intstr, 'days', 1, 31)


def zpad_months(intstr):
    """Return zero padded string."""
    return zpadlist(intstr, 'months', 1, 12)


def format_hours(intstr):
    """Return xx:00 formated time string."""
    try:
        if (int(intstr) >= 0 and int(intstr) <= 23):
            pass
        else:
            print("Invalid hours argument: {}".format(intstr))
            sys.exit()
    except TypeError:
        print("Invalid hours argument: {}".format(intstr))
        sys.exit()
    return "{}:00".format(str(intstr).zfill(2))


def format_split(splitstr):
    """Validate split argument and return argument."""
    if splitstr:
        try:
            if not splitstr.lower() in ['variable', 'year']:
                print("Invalid split argument: {}".format(splitstr))
                sys.exit()
        except TypeError:
            print("Invalid split argument: {}".format(splitstr))
            sys.exit()
        return splitstr.lower()
    else:
        return None


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
    fetch = subparsers.add_parser(
        'fetch',
        description='Execute the data fetch process.',
        formatter_class=argparse.RawTextHelpFormatter)
    info = subparsers.add_parser(
        'info',
        description='Show information on available variables and levels.',
        formatter_class=argparse.RawTextHelpFormatter)

    fetch.add_argument(
        "variables", type=str, nargs="+",
        help=textwrap.dedent('''\
                             The variable to be downloaded. See the cds
                             website or inputref.py for availabe variables.
                             '''))
    fetch.add_argument(
        "-y", "--years", type=str_seq,
        required=True,
        help=textwrap.dedent('''\
                             Year(s) for which the data should be downloaded.
                             '''))
    fetch.add_argument(
        "-m", "--months", nargs="+",
        required=False, type=zpad_months,
        default=[str(m).zfill(2) for m in list(range(1, 13))],
        help=textwrap.dedent('''\
                             Months to download data for. Defaults to all
                             months.
                             '''))
    fetch.add_argument(
        "-d", "--days", nargs="+",
        required=False, type=zpad_days,
        default=[str(d).zfill(2) for d in list(range(1, 32))],
        help=textwrap.dedent('''\
                             Days to download data for. Defaults to all days.
                             '''))
    fetch.add_argument(
        "-t", "--hours", nargs="+",
        required=False, type=format_hours,
        default=["{}:00".format(str(h).zfill(2)) for
                 h in list(range(0, 24))],
        help=textwrap.dedent('''\
                             Time of day in hours to download data for.
                             Defaults to all hours.
                             '''))
    fetch.add_argument(
        "-l", "--levels", nargs="+", type=int,
        required=False,
        help=textwrap.dedent('''\
                             Pressure levels to download for three dimensional
                             data. Default is all available levels. See the
                             cds website or inputref.py for available levels.
                             '''))
    fetch.add_argument(
        "-o", "--outputprefix", type=str, default='era5',
        help=textwrap.dedent('''\
                             Prefix of output filename. Default prefix is
                             era5.
                             '''))
<<<<<<< HEAD
    fetch.add_argument(
        "-f", "--format", type=str,
        default="netcdf", choices=["netcdf", "grib"],
        help="Output file type. Defaults to 'netcdf'.")
    fetch.add_argument(
        "-s", "--split", type=bool,
        default=True, required=False,
        help=textwrap.dedent('''
=======
    fetch.add_argument("-f", "--format", type=str,
                        default="netcdf", choices = ["netcdf", "grib"],
                        help="Output file type. Defaults to 'netcdf'.")
    fetch.add_argument("-s", "--split", type=bool,
                        default=True, required=False,
                        help=textwrap.dedent('''
>>>>>>> fix unsolved merge conflicts
                             Split output by years. Default is True.
                             '''))
    fetch.add_argument(
        "--threads", type=int, choices=range(1, 7),
        required=False, default=None,
        help=textwrap.dedent('''\
                             Number of parallel threads to use when downloading
                             using split. Default is a single process.
                             '''))
    info.add_argument(
        "type", type=str, choices=ref.refdict,
        help=textwrap.dedent('''\
                             Print lists of available variables or pressure
                             levels.
                           '''))

    args = parser.parse_args()

  # input arguments
    try:
        infotype = args.type
        try:
            print(ref.refdict[infotype])
        except KeyError:
            raise Exception('Unknown value for reference argument.')

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
<<<<<<< HEAD
    else:
        try:
            print(ref.refdict[infotype])
        except KeyError:
            raise Exception('Unknown value for reference argument.')

=======
>>>>>>> fix unsolved merge conflicts

if __name__ == "__main__":
    main()
