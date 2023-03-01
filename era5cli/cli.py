#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import sys
from datetime import datetime
import era5cli.fetch as efetch
import era5cli.info as einfo
from era5cli import args


def _build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        usage='Use "%(prog)s --help" for more information.',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="sub-command", dest="command")
    subparsers.required = True

    common = argparse.ArgumentParser(add_help=False)
    args.common.populate_common(common)

    args.periods.add_period_args(subparsers, common)

    args.info.add_info_args(subparsers)

    args.config.add_config_args(subparsers)

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


def _execute(input_args: argparse.Namespace) -> True:
    """Call to ERA-5 cli library."""
    # the info subroutine
    if input_args.command == "info":
        return _run_info(input_args)

    if input_args.command == "config":
        return args.config.config_control_flow(input_args)

    # the fetching subroutines
    years = _construct_year_list(input_args)
    synoptic, statistics, days, hours = _set_period_args(input_args)
    # try to build and send download request
    era5 = efetch.Fetch(
        years,
        months=input_args.months,
        days=days,
        hours=hours,
        variables=input_args.variables,
        area=input_args.area,
        outputformat=input_args.format,
        outputprefix=input_args.outputprefix,
        period=input_args.command,
        ensemble=input_args.ensemble,
        synoptic=synoptic,
        statistics=statistics,
        pressurelevels=input_args.levels,
        threads=input_args.threads,
        merge=input_args.merge,
        prelimbe=input_args.prelimbe,
        land=input_args.land,
    )
    era5.fetch(dryrun=input_args.dryrun)
    return True


def main(argv=None):
    """Main."""
    # get arguments
    if argv is None:
        argv = sys.argv
    args = _parse_args(argv[1:])
    _execute(args)


if __name__ == "__main__":
    main()  # pragma: no cover
