import argparse
import textwrap
from era5cli import key_management


def add_config_args(subparsers: argparse._SubParsersAction) -> None:
    """Populate the subparsers with the 'config' parser.

    The config parser allows users to view as well as set their cds API keys.

    Adds the 'config' parser with the following arguments:
        --show
        --key
        --url

    Args:
        subparsers: Subparsers to which the 'config' parser should be added to.
    """
    config = subparsers.add_parser(
        "config",
        description="",
        prog=textwrap.dedent(
            """
            Configure the CDS login info for era5cli.

            This will create a config file in your home directory, in folder named
            ".config". The CDS URL, your UID and the CDS keys will be stored here.

            To find your key, go to https://beta-cds.climate.copernicus.eu/ and
            login with your email and password. Then go to your user profile (top
            right).

            Use `era5cli config --help` for more information.
            """
        ),
        help=textwrap.dedent(
            """
            Configure the CDS login info for era5cli.

            """
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    config.add_argument(
        "--show",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Print the stored keys to the screen.
            """
        ),
    )

    config.add_argument(
        "--key",
        type=str,
        help=textwrap.dedent(
            """
            Your CDS key, e.g.: "4s215sgs-2dfa-6h34-62h2-1615ad163414"
            """
        ),
    )

    config.add_argument(
        "--url",
        type=str,
        required=False,
        default=key_management.DEFAULT_CDS_URL,
        help=textwrap.dedent(
            f"""
            (optional) URL to the CDS, by default:
                {key_management.DEFAULT_CDS_URL}
            """
        ),
    )

    config.add_argument(
        "--uid",
        type=str,
        required=False,
        default="",
        help=textwrap.dedent(
            """
            DO NOT USE: deprecated due to changes in the CDS API"
            """
        ),
    )


class InputError(Exception):
    "Raised when a user inputs an invalid combination of arguments."


def run_config(args):
    """Control flow for the config subparser.

    This custom control flow is required to implement the exclusive
    groups [show] and [uid + key (+ url)], and specifies the behavior
    of these arguments.

    Args:
        args: Arguments collected by argparse
    """
    if len(args.uid) > 0:
        msg = (
            "The `uid` argument is deprecated.\n"
            "The new CDS API does not use UIDs anymore."
        )
        raise InputError(msg)

    if args.show and args.key is not None:
        raise InputError("Either call `show` or set the key. Not both.")
    if not args.show and args.key is None:
        raise InputError("Your CDS API key is a required input.")
    if args.show:
        url, key = key_management.load_era5cli_config()
        print(
            "Contents of .config/era5cli.txt:\n" f"    key: {key}\n" f"    url: {url}\n"
        )
    else:
        key_management.set_config(args.url, args.key)
