import textwrap
from argparse import ArgumentParser
import era5cli.inputref as ref


def _level_parse(level: str) -> int:
    """Parse levels as integers, or the string 'surface'"""
    if level == "surface":
        return str(level)
    return int(level)


def populate_common(argument_parser: ArgumentParser) -> None:
    """Populate the ArgumentParser with common (shared) arguments.

    Adds the following arguments:
        --variables,
        --startyear,
        --endyear,
        --levels,
        --outputprefix,
        --format,
        --merge,
        --threads,
        --ensemble,
        --dryrun,
        --prelimbe,
        --land,
        --area,

    Args:
        argument_parser: the ArgumentParser that the arguments are added to.
    """
    argument_parser.add_argument(
        "--variables",
        type=str,
        required=True,
        nargs="+",
        help=textwrap.dedent(
            """
            The variables to download data for. This can be a
            single variable, or multiple. See the Copernicus
            Climate Data Store website or run
            `era5cli info -h` for available variables.

            """
        ),
    )

    argument_parser.add_argument(
        "--startyear",
        type=int,
        required=True,
        help=textwrap.dedent(
            """
            Single year or first year of range for which
            data should be downloaded.
            Every year will be downloaded in a separate file
            by default. Set `--split false` to change this

            """
        ),
    )

    argument_parser.add_argument(
        "--endyear",
        type=int,
        required=False,
        default=None,
        help=textwrap.dedent(
            """
            Last year of range for which data should be
            downloaded.
            If only a single year is needed, only
            `--startyear` needs to be specified.
            Every year will be downloaded in a separate file
            by default. Set `--split false` to change this

            """
        ),
    )

    argument_parser.add_argument(
        "--levels",
        nargs="+",
        type=_level_parse,
        required=False,
        default=ref.PLEVELS,
        help=textwrap.dedent(
            """
            Pressure level(s) to download 3D variables for.
            Default is all available levels. See the Copernicus
            Climate Data Store website or run `era5cli info -h`
            for available pressure levels. For geopotential,
            `--levels surface` can be used to request data from
            the single level dataset (previously called
            orography)

            """
        ),
    )

    argument_parser.add_argument(
        "--outputprefix",
        type=str,
        default="era5",
        help=textwrap.dedent(
            """
            Prefix to be used for the output filename.
            Default prefix is `era5`

            """
        ),
    )

    argument_parser.add_argument(
        "--format",
        type=str,
        default="netcdf",
        choices=["netcdf", "grib"],
        help=textwrap.dedent(
            """
            Output file type. Defaults to `netcdf`

            """
        ),
    )

    argument_parser.add_argument(
        "--merge",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Merge yearly output files.
            Default is split output files into separate files
            for every year

            """
        ),
    )

    argument_parser.add_argument(
        "--threads",
        type=int,
        choices=range(1, 7),
        required=False,
        default=None,
        help=textwrap.dedent(
            """
            Number of parallel threads to use when
            downloading. Defaults to a single process

            """
        ),
    )

    argument_parser.add_argument(
        "--ensemble",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download high resolution realisation
            (HRES) or a reduced resolution ten member ensemble
            (EDA). Providing the `--ensemble` argument
            downloads the reduced resolution ensemble.
            `--ensemble` is incompatible with `--land`

            """
        ),
    )

    argument_parser.add_argument(
        "--dryrun",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to print the cdsapi request to the screen,
            or make the request to start downloading the data.
            Providing the `--dryrun` argument will print the
            request to stdout. By default, the data will be
            downloaded

            """
        ),
    )

    argument_parser.add_argument(
        "--prelimbe",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download the preliminary back extension
            (1950-1978). Note that when `--prelimbe` is used,
            `--startyear` and `--endyear` should be set
            between 1950 and 1978. Please, be aware that
            ERA5 data is available from 1959.
            `--prelimbe` is incompatible with `--land`

            """
        ),
    )

    argument_parser.add_argument(
        "--land",
        action="store_true",
        default=False,
        help=textwrap.dedent(
            """
            Whether to download data from the ERA5-Land
            dataset. Note that the ERA5-Land dataset starts in
            1950.
            `--land` is incompatible with the use of
            `--prelimbe` and `--ensemble`

            """
        ),
    )

    argument_parser.add_argument(
        "--area",
        nargs=4,
        type=float,
        metavar=("LAT_MAX", "LON_MIN", "LAT_MIN", "LON_MAX"),
        required=False,
        help=textwrap.dedent(
            """
            Coordinates in case extraction of a subregion is
            requested.
            Specified as `LAT_MAX LON_MIN LAT_MIN LON_MAX`
            (counterclockwise coordinates, starting at the top)
            with longitude in the range -180, +180
            and latitude in the range -90, +90. For example:
            `--area 90 -180 -90 180`. Requests are rounded down
            to two decimals. By default, the entire
            available area will be returned

            """
        ),
    )
