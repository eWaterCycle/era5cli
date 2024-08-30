import argparse
import textwrap
from era5cli import utils


def add_period_args(subparsers, common):
    """Add period related parsers and arguments.

    Adds the following parsers:
        monthly, hourly.

    As well as the following arguments (for
    some of the previously mentioned parsers):
        --months, --days, --hours, --synoptic, --statistics
    """
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
        default=list(range(24)),
        help=textwrap.dedent(
            """
            Time of day in hours to download data for.
            Defaults to all hours. For every year,
            only these hours will be downloaded

            """
        ),
    )

    splitmonths = argparse.ArgumentParser(add_help=False)

    splitmonths.add_argument(
        "--splitmonths",
        type=lambda x: bool(utils.strtobool(x)),  # type=bool doesn't work.
        default=True,
        help=textwrap.dedent(
            """
            By default when downloading hourly data requests are split
            by months.
            To suppress this behavior, use: `--splitmonths False` to have yearly
            files.
            """
        ),
    )

    hourly = subparsers.add_parser(
        "hourly",
        parents=[common, mnth, day, hour, splitmonths],
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


def set_period_args(args):
    """Set subroutine specific arguments for monthly and hourly fetches."""
    if args.command == "monthly":
        statistics = None
        days = None
        splitmonths = False
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
        splitmonths: bool = args.splitmonths
        statistics: bool = args.statistics
        if statistics:
            assert args.ensemble, (
                "Statistics can only be computed over an ensemble, "
                "add --ensemble or remove --statistics."
            )
        days = args.days
        hours = args.hours
    else:
        raise AttributeError(f'The command "{args.command}" is not valid.')
    return synoptic, statistics, splitmonths, days, hours
