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
    """Execute the arguments given by the user."""

    if input_args.command == "info":
        return args.info.run_info(input_args)

    if input_args.command == "config":
        return args.config.run_config(input_args)

    # the fetching subroutines
    years = args.common.construct_year_list(input_args)
    synoptic, statistics, splitmonths, days, hours = args.periods.set_period_args(
        input_args
    )

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
        splitmonths=splitmonths,
        merge=input_args.merge,
        land=input_args.land,
        overwrite=input_args.overwrite,
        dashed_vars=input_args.dashed_varname,
        dryrun=input_args.dryrun,
    )
    era5.fetch(dryrun=input_args.dryrun)
    return True


def main(argv=None):
    """Run era5cli.

    argv is an optional kwarg to be used in testing. When called
    from the command line, the user-input arguments are retreived
    using sys.argv.
    """
    if argv is None:
        argv = sys.argv  # pragma: no cover

    # Skip the first argument (i.e. 'era5cli')
    args = _parse_args(argv[1:])
    _execute(args)


if __name__ == "__main__":
    main()  # pragma: no cover
