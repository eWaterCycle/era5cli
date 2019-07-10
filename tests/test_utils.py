"""Tests for era5cli utility functios."""

import pytest
import tempfile
from netCDF4 import Dataset
import os

import era5cli.utils
import era5cli
from era5cli.__version__ import __version__ as era5cliversion


def test_zpad_days():
    """Test zpad_days utility function."""
    # test valid input 1
    valid = list(range(1, 32))
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                    '31']
    result = era5cli.utils._zpad_days(valid)
    assert (valid_result == result)
    # test valid input 2
    valid = list(range(11, 21))
    valid_result = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    result = era5cli.utils._zpad_days(valid)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(0, 32))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_days(invalid1)
    # test invalid input 2
    invalid2 = list(range(0, 33))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpad_days(invalid2)


def test_zpad_months():
    """Test zpad_months utility function."""
    # test valid input 1
    valid1 = list(range(1, 13))
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    result = era5cli.utils._zpad_months(valid1)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ['05', '06', '07', '08', '09', '10']
    result = era5cli.utils._zpad_months(valid2)
    assert (valid_result == result)
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
    valid_result = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    result = era5cli.utils._format_hours(valid1)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(6, 12))
    valid_result = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00']
    result = era5cli.utils._format_hours(valid2)
    assert (valid_result == result)
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
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    result = era5cli.utils._zpadlist(valid1, 'days', 1, 12)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ['05', '06', '07', '08', '09', '10']
    result = era5cli.utils._zpadlist(valid2, 'days', 1, 12)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(0, 13))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpadlist(invalid1, 'days', 1, 12)
    # test invalid input 2
    invalid2 = list(range(1, 14))
    # test if exception is raised
    with pytest.raises(Exception):
        assert era5cli.utils._zpadlist(invalid2, 'days', 1, 12)


def test_print_multicolumn():
    """Test print_multicolumn utility function."""
    header = 'header'
    lst = ['unkown1', 'unkown2', 'unkown3', 'unkown4', 'unkown5', 'unkown6']
    era5cli.utils._print_multicolumn(header, lst)
    assert True


def test_append_history():
    """Test append_history utility function."""
    # test netCDF file with existing history
    (fd, filename) = tempfile.mkstemp(suffix=".nc")
    # create tmp netCDF file
    ncfile = Dataset(filename, 'w')
    orig_history = "Test history line."
    ncfile.history = orig_history
    ncfile.close()
    # test append history
    era5cli.utils._append_history(filename)
    # load netCDF file
    ncfile = Dataset(filename, 'r')
    new_history = ncfile.history
    appendtxt = "Downloaded using {} {}.".format(
        era5cli.__name__,
        era5cliversion)
    hist_split = new_history.split('\n')
    assert hist_split[0] == appendtxt
    assert hist_split[1] == orig_history
    # remove temporary file
    os.remove(filename)

    # test netCDF file without existing history
    ncfile = Dataset(filename, 'w')
    ncfile.close()
    # test append history
    era5cli.utils._append_history(filename)
    # load netCDF file
    ncfile = Dataset(filename, 'r')
    new_history = ncfile.history
    appendtxt = "Downloaded using {} {}.".format(
        era5cli.__name__,
        era5cliversion)
    new_history = appendtxt
    # remove temporary file
    os.remove(filename)
