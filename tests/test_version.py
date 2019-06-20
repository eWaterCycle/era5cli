"""Tests for era5cli __version__ available variales."""

import pytest
import era5cli.__version__ as era5cli


def test_variables():
    """Test existence of variables."""
    with pytest.raises(Exception):
        assert not era5cli.__author__
    with pytest.raises(Exception):
        assert not era5cli.__email__
    with pytest.raises(Exception):
        assert not era5cli.__version__
