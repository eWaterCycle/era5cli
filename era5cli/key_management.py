import os
import sys
from pathlib import Path
from typing import Tuple
import cdsapi
from requests.exceptions import ConnectionError  # pylint: disable=redefined-builtin


ERA5CLI_CONFIG_PATH = Path.home() / ".config" / "era5cli" / "cds_key.txt"
CDSAPI_CONFIG_PATH = Path.home() / ".cdsapirc"
DEFAULT_CDS_URL = "https://cds.climate.copernicus.eu/api"

AUTH_ERR_MSG = "401"
NO_DATA_ERR_MSG = "There is no data matching your request"


class InvalidRequestError(Exception):
    "Raised when an invalid request error is given by the cdsapi."


class InvalidLoginError(Exception):
    "Raised when an invalid login is provided to the cds server."


def attempt_cds_login(url: str, key: str) -> True:
    """Attempt to connect to the CDS, to validate the URL and UID + key.

    Args:
        url: URL to the CDS API.
        key: Combination of your UID and key, separated with a colon.

    Raises:
        ConnectionError: If no connection to the CDS could be made.
        InvalidLoginError: If an invalid authetication was provided to the CDS.
        InvalidRequestError: If the test request failed, likely due to changes in the
            CDS API's variable naming.
    """
    client = cdsapi.Client(key=key, url=url, verify=True)
    try:
        # Check the URL
        client.status()  # pragma: no cover

        # Checks if the authentication works, without downloading data
        client.retrieve(  # pragma: no cover
            "reanalysis-era5-single-levels",
            {
                "variable": "2t",
                "product_type": "reanalysis",
                "date": "2012-12-01",
                "time": "14:00",
                "data_format": "netcdf",
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
                " an incorrect key."
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
    key: str,
) -> True:
    """Check the user-input configuration. Entry point for the CLI."""
    try:
        attempt_cds_login(url, key)
        write_era5cli_config(url, key)
        print(
            f"Keys succesfully validated and stored in {ERA5CLI_CONFIG_PATH.resolve()}"
        )
        return True
    except InvalidLoginError:
        print("Error: the key is rejected by the CDS. " "Please check and try again.")
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
        url, key = load_cdsapi_config()
        try:
            if sys.stdin.isatty() and attempt_cds_login(url, key):
                userinput = input(
                    "Valid CDS keys found in the .cdsapirc file. Do you want to use "
                    "these for era5cli? [Y/n]"
                )
                if userinput.lower() in ["y", "yes", ""]:
                    set_config(url, key)
                    return True
        except (ConnectionError, InvalidLoginError, InvalidRequestError):
            return False
    return False


def load_era5cli_config() -> Tuple[str, str]:
    with open(ERA5CLI_CONFIG_PATH, encoding="utf8") as f:
        contents = "".join(f.readlines())
        if "uid:" in contents:
            msg = (
                "Old config detected. In the new CDS API only a key is required.\n"
                "Please look at the new CDS website, and reconfigure your login in "
                "era5cli\n"
                "    https://cds.climate.copernicus.eu/"
            )
            raise InvalidLoginError(msg)

    with open(ERA5CLI_CONFIG_PATH, encoding="utf8") as f:
        url = f.readline().replace("url:", "").strip()
        key = f.readline().replace("key:", "").strip()
    return url, key


def write_era5cli_config(url: str, key: str):
    ERA5CLI_CONFIG_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(ERA5CLI_CONFIG_PATH, mode="w", encoding="utf-8") as f:
        f.write(f"url: {url}\n")
        f.write(f"key: {key}\n")


def load_cdsapi_config() -> Tuple[str, str]:
    with open(CDSAPI_CONFIG_PATH, encoding="utf-8") as f:
        url = f.readline().replace("url:", "").strip()
        key = f.readline().replace("key:", "").strip()
        if ":" in key or "api/v2" in url:
            msg = (
                "Your CDS API configuration file contains a UID entry/incorrect URL.\n"
                "Please look at the new CDS website, and reconfigure your key:\n"
                "    https://cds.climate.copernicus.eu/"
            )
            raise InvalidLoginError(msg)
    return url, key
