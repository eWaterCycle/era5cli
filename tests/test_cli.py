"""Tests for era5cli utility functions."""

import unittest.mock as mock
import pytest
import era5cli.cli as cli
import era5cli.inputref as ref


def test_parse_args():
    """Test argument parser of cli."""
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2008",
        "--ensemble",
        "--land",
    ]
    args = cli._parse_args(argv)
    assert args.command == "hourly"
    assert args.days == list(range(1, 32))
    assert args.endyear == 2008
    assert args.ensemble
    assert args.format == "netcdf"
    assert args.hours == list(range(0, 24))
    assert args.levels == ref.PLEVELS
    assert args.months == list(range(1, 13))
    assert args.outputprefix == "era5"
    assert not args.merge
    assert args.startyear == 2008
    assert args.statistics
    assert not args.threads
    assert args.variables == ["total_precipitation"]
    assert args.land
    assert not args.area


def test_area_argument():
    """Test if area argument is parsed correctly."""
    # Test if area arguments are parsed correctly
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2008",
        "--ensemble",
        "--area",
        "90",
        "-180",
        "-90",
        "180",
    ]
    args = cli._parse_args(argv)
    assert args.area == [90, -180, -90, 180]

    # Check that area defaults to None
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2008",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    assert not args.area

    # Requires four values
    with pytest.raises(SystemExit):
        argv = [
            "hourly",
            "--startyear",
            "2008",
            "--variables",
            "total_precipitation",
            "--statistics",
            "--endyear",
            "2008",
            "--ensemble",
            "--area",
            "90",
            "-180",
            "-90",
        ]
        cli._parse_args(argv)

    # A value cannot be missing
    with pytest.raises(SystemExit):
        argv = [
            "hourly",
            "--startyear",
            "2008",
            "--variables",
            "total_precipitation",
            "--statistics",
            "--endyear",
            "2008",
            "--ensemble",
            "--area",
            "90",
            "-180",
            "-90",
            "",
        ]
        cli._parse_args(argv)

    # Values must be numeric
    with pytest.raises(SystemExit):
        argv = [
            "hourly",
            "--startyear",
            "2008",
            "--variables",
            "total_precipitation",
            "--statistics",
            "--endyear",
            "2008",
            "--ensemble",
            "--area",
            "90",
            "-180",
            "-90",
            "E",
        ]
        cli._parse_args(argv)


def test_period_args():
    """Test the period specific argument setter with synoptic options."""
    argv = [
        "monthly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--endyear",
        "2008",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    period_args = cli._set_period_args(args)
    # Period_args consists of (synoptic, statistics, days, hours)
    assert period_args == (None, None, None, [0])

    argv = [
        "monthly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--synoptic",
        "4",
        "7",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    period_args = cli._set_period_args(args)
    # Period_args consists of (synoptic, statistics, days, hours)
    assert period_args == (True, None, None, [4, 7])

    argv = [
        "monthly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--synoptic",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    period_args = cli._set_period_args(args)
    # Period_args consists of (synoptic, statistics, days, hours)
    assert period_args == (True, None, None, range(0, 24))

    # test whether the info option does not end up in _set_period_args
    argv = ["info", "2Dvars"]
    args = cli._parse_args(argv)
    with pytest.raises(AttributeError):
        assert cli._set_period_args(args)


def test_level_arguments():
    """Test if levels are parsed correctly"""
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "geopotential",
        "--levels",
        "surface",
    ]
    args = cli._parse_args(argv)
    assert args.levels == ["surface"]

    # only numeric values or 'surface' are accepted levels
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "geopotential",
        "--levels",
        "somethingelse",
    ]
    with pytest.raises(SystemExit):
        args = cli._parse_args(argv)


@mock.patch("era5cli.fetch.Fetch", autospec=True)
def test_main_fetch(fetch):
    """Test if Fetch part of main completes without error."""
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2008",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    assert cli._execute(args)

    # should give an AssertionError if endyear is before startyear
    argv = [
        "hourly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2007",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    with pytest.raises(AssertionError):
        assert cli._execute(args)

    # should give an AssertionError if years are out of bounds
    argv = [
        "hourly",
        "--startyear",
        "1949",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2007",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    with pytest.raises(AssertionError):
        assert cli._execute(args)

    # should give an AssertionError if years are out of bounds
    argv = [
        "hourly",
        "--startyear",
        "1950",
        "--variables",
        "total_precipitation",
        "--statistics",
        "--endyear",
        "2007",
        "--ensemble",
        "--prelimbe",
    ]
    args = cli._parse_args(argv)
    with pytest.raises(AssertionError):
        assert cli._execute(args)

    # monthly call without endyear
    argv = [
        "monthly",
        "--startyear",
        "2008",
        "--variables",
        "total_precipitation",
        "--synoptic",
        "--ensemble",
    ]
    args = cli._parse_args(argv)
    cli._execute(args)


@mock.patch("era5cli.info.Info", autospec=True)
def test_main_info(info):
    """Test if Info part of main completes without error."""
    info.return_value.infotype = "list"
    argv = ["info", "levels"]
    args = cli._parse_args(argv)
    cli._execute(args)

    info.return_value.infotype = "total_precipitation"
    argv = ["info", "total_precipitation"]
    args = cli._parse_args(argv)
    cli._execute(args)


config_args = [
        "config",
        "--uid",
        "123456",
        "--key",
        "abc-def",
    ]


def test_config_parse():
    args = cli._parse_args(config_args)
    assert args.uid == "123456"
    assert args.key == "abc-def"


@mock.patch("era5cli.key_management.attempt_cds_login", return_value=True)
@mock.patch("era5cli.key_management.write_era5cli_config")
def test_config_write(mock_a, mock_b):
    args = cli._parse_args(config_args)
    cli._execute(args)
