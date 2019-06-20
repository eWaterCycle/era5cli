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


def test_print_multicolumn():
    """Test _print_multicolumn function of Info class."""
    era5info = info.Info('levels')
    era5info._define_table_header()
    era5info._print_multicolumn()
    assert True


def test_list():
    """Test list function of Info class."""
    era5info = info.Info('levels')
    era5info.list()
    assert True
