"""Tests for era5cli Fetch class."""
import pytest

from era5cli import info


INFO_PARAMS = ['levels', '2Dvars', '3Dvars', 'land',
               'total_precipitation', 'temperature']


@pytest.mark.parametrize('arg', INFO_PARAMS)
def test_init(arg):
    """Test init function of Info class."""
    era5info = info.Info(arg)
    assert isinstance(era5info.infolist, list)


@pytest.mark.parametrize('arg', ['levels', '2Dvars', '3Dvars', 'land'])
def test_define_table_header(arg):
    """Test _define_table_header function of Info class."""
    era5info = info.Info(arg)
    era5info._define_table_header()
    assert isinstance(era5info.header, str)


@pytest.mark.parametrize('arg', ['levels', '2Dvars', '3Dvars', 'land'])
def test_list(arg):
    """Test list function of Info class."""
    era5info = info.Info(arg)
    era5info.list()
    assert True


def test_vars(capsys):
    """Test vars function of Info class."""
    era5info = info.Info('total_precipitation')
    era5info.vars()
    captured = capsys.readouterr()
    assert '2Dvars' in captured.out
    assert 'land' in captured.out
    assert not '3Dvars' in captured.out
    del era5info, captured

    era5info = info.Info(850)
    era5info.vars()
    captured = capsys.readouterr()
    assert 'levels' in captured.out
    del era5info, captured
