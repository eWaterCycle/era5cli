import argparse
import textwrap
import era5cli.info


def add_info_args(subparsers):
    """Add info parser and arguments.

    Adds the 'info' parser, with the 'name' argument.
    """
    info = subparsers.add_parser(
        "info",
        description="Show information on available variables and levels.",
        prog=textwrap.dedent(
            """
            Use `era5cli info --help` for more information

            """
        ),
        help=textwrap.dedent(
            """
            Show information on available variables or levels.
            Use `era5cli info --help` for more information

            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    info.add_argument(
        "name",
        type=str,
        help=textwrap.dedent(
            """
            Enter list name to print info list: \n
            `levels` for all available pressure levels \n
            `2Dvars` for all available single level or 2D
            variables \n
            `3Dvars` for all available 3D variables \n
            `land` for all available variables in
            ERA5-land \n
            Enter variable name (e.g. `total_precipitation`)
            or pressure level (e.g. `825`) to show if the
            variable or level is available, and in which list

            """
        ),
    )


def run_info(args):
    # List dataset information
    era5info = era5cli.info.Info(args.name)
    if era5info.infotype == "list":
        era5info.list()
        return True
    era5info.vars()
    return True
