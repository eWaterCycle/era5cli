"""Tests for era5cli utility functions."""

import pytest
from netCDF4 import Dataset
import era5cli
import era5cli.utils
from era5cli.__version__ import __version__ as era5cliversion


def test_zpad_days():
    """Test zpad_days utility function."""
    # test valid input 1
    valid = list(range(1, 32))
    # fmt: off
    valid_result = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26",
        "27", "28", "29", "30", "31",
    ]  # fmt: on
    result = era5cli.utils._zpad_days(valid)
    assert valid_result == result
    # test valid input 2
    valid = list(range(11, 21))
    valid_result = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    result = era5cli.utils._zpad_days(valid)
    assert valid_result == result
    # test invalid input 1
    invalid1 = list(range(32))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_days(invalid1)
    # test invalid input 2
    invalid2 = list(range(33))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_days(invalid2)


def test_zpad_months():
    """Test zpad_months utility function."""
    # test valid input 1
    valid1 = list(range(1, 13))
    # fmt: off
    valid_result = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"
    ]  # fmt: on
    result = era5cli.utils._zpad_months(valid1)
    assert valid_result == result
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ["05", "06", "07", "08", "09", "10"]
    result = era5cli.utils._zpad_months(valid2)
    assert valid_result == result
    # test invalid input 1
    invalid1 = list(range(0, 13))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_months(invalid1)
    # test invalid input 2
    invalid2 = list(range(1, 14))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_months(invalid2)


def test_format_hours():
    """Test format_hours utility function."""
    # test valid input 1
    valid1 = list(range(0, 24))
    # fmt: off
    valid_result = [
        "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
    ]  # fmt: on
    result = era5cli.utils._format_hours(valid1)
    assert valid_result == result
    # test valid input 2
    valid2 = list(range(6, 12))
    valid_result = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"]
    result = era5cli.utils._format_hours(valid2)
    assert valid_result == result
    # test invalid input 1
    invalid1 = list(range(-1, 24))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_months(invalid1)
    # test invalid input 2
    invalid2 = list(range(0, 25))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_months(invalid2)


def test_zpadlist():
    """Test zpadlist utility function."""
    valid1 = list(range(1, 13))
    # fmt: off
    valid_result = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"
    ]  # fmt: on
    result = era5cli.utils._zpadlist(valid1, "days", 1, 12)
    assert valid_result == result
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ["05", "06", "07", "08", "09", "10"]
    result = era5cli.utils._zpadlist(valid2, "days", 1, 12)
    assert valid_result == result
    # test invalid input 1
    invalid1 = list(range(0, 13))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpadlist(invalid1, "days", 1, 12)
    # test invalid input 2
    invalid2 = list(range(1, 14))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpadlist(invalid2, "days", 1, 12)


def test_print_multicolumn():
    """Test print_multicolumn utility function."""
    header = "header"
    lst = ["unkown1", "unkown2", "unkown3", "unkown4", "unkown5", "unkown6"]
    era5cli.utils.print_multicolumn(header, lst)
    assert True


def testappend_history(tmp_path):
    """Test append_history utility function."""
    # test netCDF file with existing history
    filename = tmp_path / "dummy.nc"
    name = "reanalysis-era5-single-levels"
    request = "request"
    # create tmp netCDF file
    ncfile = Dataset(filename, "w")
    orig_history = "Test history line."
    ncfile.history = orig_history
    ncfile.close()
    # test append history
    era5cli.utils.append_history(name, request, filename)
    # load netCDF file
    ncfile = Dataset(filename, "r")
    new_history = ncfile.history
    appendtxt = f"Downloaded using {era5cli.__name__} {era5cliversion}."
    hist_split = new_history.split("\n")
    assert hist_split[0].split()[-2:] == [name, request]
    assert hist_split[1] == orig_history

    # test netCDF file without existing history
    dummy_file2 = tmp_path / "dummy2.nc"
    ncfile = Dataset(dummy_file2, "w")
    ncfile.close()
    # test append history
    era5cli.utils.append_history(name, request, dummy_file2)
    # load netCDF file
    ncfile = Dataset(dummy_file2, "r")
    new_history = ncfile.history
    appendtxt = f"Downloaded using {era5cli.__name__} {era5cliversion}."
    new_history = appendtxt


@pytest.mark.parametrize(
    "value, expected",
    [
        ("True", True),
        ("true", True),
        ("Yes", True),
        ("y", True),
        ("1", True),
        ("False", False),
        ("false", False),
        ("No", False),
        ("n", False),
        ("0", False),
    ]
)
def test_strtobool(value, expected):
    """Test correct inputs."""
    assert era5cli.utils.strtobool(value) == expected

@pytest.mark.parametrize(
    "value", ["tr", "01", "maybe", "Fals"]
)
def test_strtobool_incorrect(value):
    """Test incorrect inputs."""
    with pytest.raises(ValueError, match="Could not convert string to boolean"):
        era5cli.utils.strtobool(value)
