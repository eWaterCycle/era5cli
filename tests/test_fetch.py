"""Tests for era5cli Fetch class."""

from era5cli import fetch


def test_init():
    """Test init function of Fetch class."""
    era5 = fetch.Fetch('2008', '01', '01', '12', 'total_precipitation',
                       'netcdf', 'era5', True, 4)
    assert era5.ext == "nc"  # check correct extension
