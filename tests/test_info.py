"""Tests for era5cli Fetch class."""

from era5cli import info


def test_init():
    """Test init function of Info class."""
    era5info = info.Info('levels')
    assert isinstance(era5info.infolist, list)


def test_define_table_header():
    """Test _define_table_header function of Info class."""
    era5info = info.Info('levels')
    era5info._define_table_header()
    assert isinstance(era5info.header, str)


def test_list():
    """Test list function of Info class."""
    era5info = info.Info('levels')
    era5info.list()
    assert True


def test_vars(capsys):
    """Test vars function of Info class."""
    era5info = info.Info('total_precipitation')
    era5info.vars()
    captured = capsys.readouterr()
    assert captured.out.split(' ')[-1].strip() == '2Dvars'
    del era5info, captured

    era5info = info.Info(850)
    era5info.vars()
    captured = capsys.readouterr()
    assert captured.out.split(' ')[-1].strip() == 'levels'
    del era5info, captured
