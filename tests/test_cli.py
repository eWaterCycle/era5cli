"""Tests for era5cli utility functios."""

import era5cli.cli as cli


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
    assert not args.levels
    assert args.months == list(range(1, 13))
    assert args.outputprefix == 'era5'
    assert args.split
    assert args.startyear == 2008
    assert args.statistics
    assert not args.threads
    assert args.variables == ['total_precipitation']
