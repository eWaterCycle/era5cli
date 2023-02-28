import argparse
import textwrap


def add_period_args(subparsers, common):
    """Add period related parsers and arguments.

    Adds the following parsers:
        monthly, daily, houry.

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

    hourly = subparsers.add_parser(
        "hourly",
        parents=[common, mnth, day, hour],
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
