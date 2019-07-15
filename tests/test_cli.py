"""Tests for era5cli utility functios."""

import era5cli.cli as cli
import era5cli.inputref as ref
import unittest.mock as mock
import pytest


def test_str2bool():
    """Test str2bool cli utility function."""
    for f in ['No', 'False', 'F', 'N', '0']:
        assert not cli._str2bool(f)
    for t in ['Yes', 'True', 'T', 'Y', '1']:
        assert cli._str2bool(t)


def test_parse_args():
    """Test argument parser of cli."""
    argv = ['hourly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation', '--statistics', 'true',
            '--split', 'true', '--endyear', '2008', '--ensemble', 'true']
    args = cli._parse_args(argv)
    assert args.command == 'hourly'
    assert args.days == list(range(1, 32))
    assert args.endyear == 2008
    assert args.ensemble
    assert args.format == 'netcdf'
    assert args.hours == list(range(0, 24))
    assert args.levels == ref.PLEVELS
    assert args.months == list(range(1, 13))
    assert args.outputprefix == 'era5'
    assert args.split
    assert args.startyear == 2008
    assert args.statistics
    assert not args.threads
    assert args.variables == ['total_precipitation']


def test_period_args():
    """Test the period specific argument setter with synoptic options."""
    argv = ['monthly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation',
            '--endyear', '2008', '--ensemble', 'true']
    args = cli._parse_args(argv)
    period_args = cli._set_period_args(args)
    # Period_args consists of (synoptic, statistics, days, hours)
    assert period_args == (None, None, None, [0])

    argv = ['monthly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation',
            '--synoptic', '4', '7', '--ensemble', 'true']
    args = cli._parse_args(argv)
    period_args = cli._set_period_args(args)
    # Period_args consists of (synoptic, statistics, days, hours)
    assert period_args == (True, None, None, [4, 7])

    # test whether the info option does not end up in _set_period_args
    argv = ['info', '2Dvars']
    args = cli._parse_args(argv)
    with pytest.raises(AttributeError):
        assert cli._set_period_args(args)


@mock.patch("era5cli.fetch.Fetch", autospec=True)
def test_main_fetch(fetch):
    """Test if Fetch part of main completes without error."""
    argv = ['hourly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation', '--statistics', 'true',
            '--split', 'true', '--endyear', '2008', '--ensemble', 'true']
    args = cli._parse_args(argv)
    assert cli._execute(args)

    # should give an AssertionError if endyear is before startyear
    argv = ['hourly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation', '--statistics', 'true',
            '--split', 'true', '--endyear', '2007', '--ensemble', 'true']
    args = cli._parse_args(argv)
    with pytest.raises(AssertionError):
        assert cli._execute(args)

    # monthly call without endyear
    argv = ['monthly', '--startyear', '2008', '--ensemble', 'false',
            '--variables', 'total_precipitation', '--synoptic',
            '--split', 'true', '--ensemble', 'true']
    args = cli._parse_args(argv)
    cli._execute(args)


@mock.patch("era5cli.info.Info", autospec=True)
def test_main_info(info):
    """Test if Info part of main completes without error."""
    info.return_value.infotype = 'list'
    argv = ['info', 'levels']
    args = cli._parse_args(argv)
    cli._execute(args)

    info.return_value.infotype = 'total_precipitation'
    argv = ['info', 'total_precipitation']
    args = cli._parse_args(argv)
    cli._execute(args)
