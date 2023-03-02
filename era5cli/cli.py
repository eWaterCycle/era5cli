#!/usr/bin/env python
"""Download ERA5 variables."""

import argparse
import sys
import era5cli.fetch as efetch
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
    args.common.add_common_args(common)

    args.periods.add_period_args(subparsers, common)

    args.info.add_info_args(subparsers)

    args.config.add_config_args(subparsers)

    return parser


def _parse_args(args):
    """Parse command line arguments."""
    parser = _build_parser()
    return parser.parse_args(args)


def _execute(input_args: argparse.Namespace) -> True:
    """Call to ERA-5 cli library."""

    if input_args.command == "info":
        return args.info.run_info(input_args)

    if input_args.command == "config":
        return args.config.config_control_flow(input_args)

    # the fetching subroutines
    years = args.common.construct_year_list(input_args)
    synoptic, statistics, days, hours = args.periods.set_period_args(input_args)

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
