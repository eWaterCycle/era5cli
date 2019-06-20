"""Tests for era5cli utility functios."""

import pytest
from era5cli.utils import zpadlist
from era5cli.utils import zpad_days
from era5cli.utils import zpad_months
from era5cli.utils import format_hours
from era5cli.utils import print_multicolumn


def test_zpad_days():
    """Test zpad_days utility function."""
    # test valid input 1
    valid = list(range(1, 32))
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                    '31']
    result = zpad_days(valid)
    assert (valid_result == result)
    # test valid input 2
    valid = list(range(11, 21))
    valid_result = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    result = zpad_days(valid)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(0, 32))
    with pytest.raises(Exception):
        assert zpad_days(invalid1)  # test if exception is raised
    # test invalid input 2
    invalid2 = list(range(0, 33))
    with pytest.raises(Exception):
        assert zpad_days(invalid2)  # test if exception is raised


def test_zpad_months():
    """Test zpad_months utility function."""
    # test valid input 1
    valid1 = list(range(1, 13))
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    result = zpad_months(valid1)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ['05', '06', '07', '08', '09', '10']
    result = zpad_months(valid2)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(0, 13))
    with pytest.raises(Exception):
        assert zpad_months(invalid1)  # test if exception is raised
    # test invalid input 2
    invalid2 = list(range(1, 14))
    with pytest.raises(Exception):
        assert zpad_months(invalid2)  # test if exception is raised


def test_format_hours():
    """Test format_hours utility function."""
    # test valid input 1
    valid1 = list(range(0, 24))
    valid_result = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    result = format_hours(valid1)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(6, 12))
    valid_result = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00']
    result = format_hours(valid2)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(-1, 24))
    with pytest.raises(Exception):
        assert zpad_months(invalid1)  # test if exception is raised
    # test invalid input 2
    invalid2 = list(range(0, 25))
    with pytest.raises(Exception):
        assert zpad_months(invalid2)  # test if exception is raised


def test_zpadlist():
    """Test zpadlist utility function."""
    valid1 = list(range(1, 13))
    valid_result = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    result = zpadlist(valid1, 'days', 1, 12)
    assert (valid_result == result)
    # test valid input 2
    valid2 = list(range(5, 11))
    valid_result = ['05', '06', '07', '08', '09', '10']
    result = zpadlist(valid2, 'days', 1, 12)
    assert (valid_result == result)
    # test invalid input 1
    invalid1 = list(range(0, 13))
    with pytest.raises(Exception):
        assert zpadlist(invalid1, 'days', 1, 12)  # test if exception is raised
    # test invalid input 2
    invalid2 = list(range(1, 14))
    with pytest.raises(Exception):
        assert zpadlist(invalid2, 'days', 1, 12)  # test if exception is raised


def test_print_multicolumn():
    """Test _print_multicolumn function of Info class."""
    header = 'header'
    lst = ['unkown1', 'unkown2', 'unkown3', 'unkown4', 'unkown5', 'unkown6']
    print_multicolumn(header, lst)
    assert True
