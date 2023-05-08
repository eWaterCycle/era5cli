import os
import sys
from pathlib import Path
from typing import Tuple
import cdsapi
from requests.exceptions import ConnectionError  # pylint: disable=redefined-builtin


ERA5CLI_CONFIG_PATH = Path.home() / ".config" / "era5cli" / "cds_key.txt"
CDSAPI_CONFIG_PATH = Path.home() / ".cdsapirc"
DEFAULT_CDS_URL = "https://cds.climate.copernicus.eu/api/v2"

AUTH_ERR_MSG = "401 Authorization Required"
NO_DATA_ERR_MSG = "There is no data matching your request"


class InvalidRequestError(Exception):
    "Raised when an invalid request error is given by the cdsapi."


class InvalidLoginError(Exception):
    "Raised when an invalid login is provided to the cds server."


def attempt_cds_login(url: str, fullkey: str) -> True:
    """Attempt to connect to the CDS, to validate the URL and UID + key.

    Args:
        url: URL to the CDS API.
        fullkey: Combination of your UID and key, separated with a colon.

    Raises:
        ConnectionError: If no connection to the CDS could be made.
        InvalidLoginError: If an invalid authetication was provided to the CDS.
        InvalidRequestError: If the test request failed, likely due to changes in the
            CDS API's variable naming.

    Returns:
        True if a connection was made succesfully.
    """
    connection = cdsapi.Client(
        url=url,
        key=fullkey,
        verify=True,
        quiet=True,  # Supress output to the console from the test retrieve.
    )

    try:
        # Check the URL
        connection.status()  # pragma: no cover

        # Checks if the authentication works, without downloading data
        connection.retrieve(  # pragma: no cover
            "reanalysis-era5-single-levels",
            {
                "variable": "2t",
                "product_type": "reanalysis",
                "date": "2012-12-01",
                "time": "14:00",
                "format": "netcdf",
            },
        )
        return True

    except ConnectionError as err:
        raise ConnectionError(
            f"{os.linesep}Failed to connect to CDS. Please check your internet "
            "connection and/or the"
            f" URL in the era5cli configuration: {ERA5CLI_CONFIG_PATH.resolve()}"
            f"{os.linesep}Or redefine your configuration with 'era5cli config'"
        ) from err

    except Exception as err:
        if AUTH_ERR_MSG in str(err):
            raise InvalidLoginError(
                f"{os.linesep}Authorization with the CDS served failed. Likely due to"
                " an incorrect key or UID."
                f"{os.linesep}Please check your era5cli configuration file: "
                f"{ERA5CLI_CONFIG_PATH.resolve()}{os.linesep}"
                "Or redefine your configuration with 'era5cli config'"
            ) from err
        if NO_DATA_ERR_MSG in str(err):
            raise InvalidRequestError(
                f"{os.linesep}Something changed in the CDS API. Please raise an issue "
                "on https://www.github.com/eWaterCycle/era5cli"
            ) from err
        raise err  # pragma: no cover


def set_config(
    url: str,
    uid: str,
    key: str,
) -> True:
    """Check the user-input configuration. Entry point for the CLI."""
    try:
        attempt_cds_login(url, fullkey=f"{uid}:{key}")
        write_era5cli_config(url, uid, key)
        print(
            f"Keys succesfully validated and stored in {ERA5CLI_CONFIG_PATH.resolve()}"
        )
        return True
    except InvalidLoginError:
        print(
            "Error: the UID and key are rejected by the CDS. "
            "Please check and try again."
        )
    return False


def check_era5cli_config() -> None:
    """Validate if the era5cli config exists, and can connect to the CDS.

    If no era5cli config file exists, but a CDS api file exists in the default location,
    This routine will attempt to use those keys, and ask the user if they want to use
    these.
    """
    if ERA5CLI_CONFIG_PATH.exists():
        url, fullkey = load_era5cli_config()
        attempt_cds_login(url, fullkey)
    else:
        print("era5cli configuration file not found. Looking for CDSAPI key.")
        if not valid_cdsapi_config():
            raise InvalidLoginError(
                "No valid CDS login found. Please configure your CDS login using: "
                "'era5cli config'"
            )


def valid_cdsapi_config() -> bool:
    """Validate the default cdsapirc file. Promts the user for using these for era5cli.

    Returns:
        True if a valid key has been found & written to file. Otherwise False.
    """
    if CDSAPI_CONFIG_PATH.exists():
        url, fullkey = load_cdsapi_config()
        try:
            if sys.stdin.isatty() and attempt_cds_login(url, fullkey):
                userinput = input(
                    "Valid CDS keys found in the .cdsapirc file. Do you want to use "
                    "these for era5cli? [Y/n]"
                )
                if userinput in ["Y", "y", "Yes", "yes"]:
                    set_config(
                        url, uid=fullkey.split(":")[0], key=fullkey.split(":")[1]
                    )
                    return True
        except (ConnectionError, InvalidLoginError, InvalidRequestError):
            return False
    return False


def load_era5cli_config() -> Tuple[str, str]:
    with open(ERA5CLI_CONFIG_PATH, encoding="utf8") as f:
        url = f.readline().replace("url:", "").strip()
        uid = f.readline().replace("uid:", "").strip()
        key = f.readline().replace("key:", "").strip()
    return url, f"{uid}:{key}"


def write_era5cli_config(url: str, uid: str, key: str):
    ERA5CLI_CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(ERA5CLI_CONFIG_PATH, mode="w", encoding="utf-8") as f:
        f.write(f"url: {url}\n")
        f.write(f"uid: {uid}\n")
        f.write(f"key: {key}\n")


def load_cdsapi_config() -> Tuple[str, str]:
    with open(CDSAPI_CONFIG_PATH, encoding="utf-8") as f:
        url = f.readline().replace("url:", "").strip()
        fullkey = f.readline().replace("key:", "").strip()
    return url, fullkey
