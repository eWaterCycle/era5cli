"""Module to compute the size of the CDS request."""

from typing import TYPE_CHECKING
from era5cli import inputref


if TYPE_CHECKING:
    from era5cli.fetch import Fetch


# The following "MAX_REQUESTS" come from the cds.climate.copernicus.eu
# api request generator. On the CDS one 'request' represents one 2D 'image' of the data
# i.e. one variable, at one timestep, at one (pressure)level.
# Single- and multi- level variables have a limit of 120.000 requests, while ERA5-land
# is limited to 1000, likely due to the higher spatial resolution.
MAX_REQUESTS = 120000  # Maximum requests for non-land data
MAX_REQUESTS_LAND = 1000  # Max requests for "reanalysis-era5-land"
VALID_HOURS_ENSEMBLE = [0, 3, 6, 9, 12, 15, 18, 21]


class TooLargeRequestError(Exception):
    """Raised when a request is too big for the CDS."""


def n_hours(fetch: "Fetch") -> int:
    """Get the number of hours in a request."""
    if fetch.ensemble:
        return sum(hr in fetch.hours for hr in VALID_HOURS_ENSEMBLE)
    return len(fetch.hours)


def request_too_large(fetch: "Fetch") -> bool:
    """Determine if a request will raise a Too Large Request error at the CDS."""
    n_months = 1 if fetch.splitmonths else len(fetch.months)

    # Each time step counts as a request
    request_size = n_months * len(fetch.days) * n_hours(fetch)

    if fetch.land:
        return True if request_size > MAX_REQUESTS_LAND else False

    # Every pressure level is a separate request
    if any([var in inputref.PLVARS for var in fetch.variables]):
        request_size *= len(fetch.pressure_levels)

    # Each (ensemble) statistic counts as a separate request
    if fetch.statistics:
        request_size *= 3  # Mean and spread are added.

    return True if request_size > MAX_REQUESTS else False
