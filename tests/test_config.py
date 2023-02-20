from unittest.mock import patch
import pytest
from era5cli import key_management


@pytest.fixture(scope="function")
def config_path_era5(tmp_path_factory):
    return tmp_path_factory.mktemp(".config") / "era5cli.txt"


@pytest.fixture(scope="function")
def config_path_cds(tmp_path_factory):
    fn = tmp_path_factory.mktemp(".config") / ".cdsapirc"
    with open(fn, mode="w", encoding="utf-8") as f:
        f.write("url: a\nkey: 123:abc-def")
    return fn


class TestConfig:
    def test_check_cdsrc_no(self, config_path_era5, config_path_cds):
        """.cdsapirc exists. User says no. Should raise InvalidLoginError"""
        with (
            patch("builtins.input", return_value="N"),
            patch("era5cli.key_management.attempt_cds_login", return_value=True),
            patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", config_path_era5),
            patch("era5cli.key_management.CDSAPI_CONFIG_PATH", config_path_cds),
        ):
            with pytest.raises(key_management.InvalidLoginError):
                key_management.check_era5cli_config()

    def test_check_cdsrc_yes(self, config_path_era5, config_path_cds):
        """.cdsapirc exists. User says yes. url+key is copied to the era5cli config."""
        with (
            patch("builtins.input", return_value="Y"),
            patch("era5cli.key_management.attempt_cds_login", return_value=True),
            patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", config_path_era5),
            patch("era5cli.key_management.CDSAPI_CONFIG_PATH", config_path_cds),
        ):
            key_management.check_era5cli_config()
            with open(config_path_era5, "r", encoding="utf-8") as f:
                assert f.readlines() == ["url: a\n", "uid: 123\n", "key: abc-def\n"]
