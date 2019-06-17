#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import textwrap
import sys
from era5cli.fetch import Fetch


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
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-y", "--years", type=str_seq, nargs="+",
                        required=True,
                        help=textwrap.dedent('''
                             Year(s) for which the data should be downloaded.
                             '''))
    parser.add_argument("-m", "--months", nargs="+",
                        required=False, type=zpad_months,
                        default=[str(m).zfill(2) for m in list(range(1, 13))],
                        help=textwrap.dedent('''
                             Months to download data for. Defaults to all
                             months.
                             '''))
    parser.add_argument("-d", "--days", nargs="+",
                        required=False, type=zpad_days,
                        default=[str(d).zfill(2) for d in list(range(1, 32))],
                        help=textwrap.dedent('''
                             Days to download data for. Defaults to all days.
                             '''))
    parser.add_argument("-t", "--hours", nargs="+",
                        required=False, type=format_hours,
                        default=["{}:00".format(str(h).zfill(2)) for
                                 h in list(range(0, 24))],
                        help=textwrap.dedent('''
                             Time of day in hours to download data for.
                             Defaults to all hours.
                             '''))
    parser.add_argument("-p", "--variables", type=str, nargs="+",
                        required=True,
                        help=textwrap.dedent('''
                             The variable to be downloaded. See the cds
                             website for availabe variables.
                             '''))
    parser.add_argument("-o", "--outputprefix", type=str, default='era5',
                        help=textwrap.dedent('''
                             Prefix of output filename. Default prefix is
                             era5.
                             '''))
    parser.add_argument("-f", "--format", type=str,
                        default="netcdf",
                        help="Output file type. Defaults to 'netcdf'.")
    parser.add_argument("-s", "--split", type=str2bool,
                        default=True,
                        required=False, help="Split output by years. Default splits by variables and years.")
    parser.add_argument("--threads", type=int,
                        required=False, default=None,
                        help=textwrap.dedent('''
                             Number of parallel threads to use when downloading
                             using split.
                             '''))
    args = parser.parse_args()

    # input arguments
    variables = args.variables
    months = args.months
    days = args.days
    hours = args.hours
    split = args.split
    outputformat = args.format
    threads = args.threads
    # flatten years list
    yrset = set([item for sublist in args.years for item in sublist])
    years = list(yrset)
    outputprefix = args.outputprefix

    # Fetch the data
    era5 = Fetch(years, months, days, hours, variables, outputformat,
                 outputprefix, split, threads)
    era5.fetch()


if __name__ == "__main__":
    main()
