from unittest.mock import patch
import pytest
import requests.exceptions as rex
from era5cli import key_management


CFG_FILE = "url: https://www.github.com/\nkey: abc-def\n"


@pytest.fixture(scope="function")
def empty_path_era5(tmp_path_factory):
    return tmp_path_factory.mktemp("usrhome") / ".config" / "era5cli" / "cds_keys.txt"


@pytest.fixture(scope="function")
def valid_path_era5(tmp_path_factory):
    fn = tmp_path_factory.mktemp(".config") / "era5cli" / "cds_keys.txt"
    fn.parent.mkdir(parents=True)
    with open(fn, mode="w", encoding="utf-8") as f:
        f.write(CFG_FILE)
    return fn


@pytest.fixture(scope="function")
def empty_path_cds(tmp_path_factory):
    return tmp_path_factory.mktemp(".config") / "cdsapirc.txt"


@pytest.fixture(scope="function")
def valid_path_cds(tmp_path_factory):
    fn = tmp_path_factory.mktemp(".config") / "cdsapirc.txt"
    with open(fn, mode="w", encoding="utf-8") as f:
        f.write(CFG_FILE)
    return fn


class TestEra5CliConfig:
    """Test the functionality for writing and loading the config file."""

    def test_set_config(self, empty_path_era5):
        with patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", empty_path_era5):
            key_management.write_era5cli_config(url="b", key="abc-def")
            assert key_management.load_era5cli_config() == ("b", "abc-def")

    def test_load_era5cli_config(self, valid_path_era5):
        with patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", valid_path_era5):
            assert key_management.load_era5cli_config() == (
                "https://www.github.com/",
                "abc-def",
            )

    def test_check_era5cli_config(self, valid_path_era5):
        mp1 = patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", valid_path_era5)
        mp2 = patch("era5cli.key_management.attempt_cds_login", return_value=True)
        with mp1, mp2:
            key_management.check_era5cli_config()

    def test_old_config(self, empty_path_era5):
        with patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", empty_path_era5):
            key_management.write_era5cli_config(url="b", key="uid:abc-def")
            with pytest.raises(key_management.InvalidLoginError, match="Old config"):
                key_management.load_era5cli_config()


class TestConfigCdsrc:
    """Test the cases where a .cdsapirc file exists.

    This leads to three options:
        - File exists, the keys are valid, and user does not want to copy the keys.
        - File exists, the keys are valid, and the users wants to copy the keys.
        - File exists, and the keys are not valid.
    """

    def test_cdsrcfile_user_says_no(self, empty_path_era5, valid_path_cds):
        """.cdsapirc exists. User says no. Should raise InvalidLoginError"""
        mp1 = patch("builtins.input", return_value="N")
        mp2 = patch("era5cli.key_management.attempt_cds_login", return_value=True)
        mp3 = patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", empty_path_era5)
        mp4 = patch("era5cli.key_management.CDSAPI_CONFIG_PATH", valid_path_cds)
        mp5 = patch("sys.stdin.isatty", return_value=True)
        with mp1, mp2, mp3, mp4, mp5:
            with pytest.raises(
                key_management.InvalidLoginError, match="No valid CDS login found"
            ):
                key_management.check_era5cli_config()

    def test_cdsrcfile_user_says_yes(self, empty_path_era5, valid_path_cds):
        """.cdsapirc exists. User says yes. url+key is copied to the era5cli config."""
        mp1 = patch("builtins.input", return_value="Y")
        mp2 = patch("era5cli.key_management.attempt_cds_login", return_value=True)
        mp3 = patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", empty_path_era5)
        mp4 = patch("era5cli.key_management.CDSAPI_CONFIG_PATH", valid_path_cds)
        mp5 = patch("sys.stdin.isatty", return_value=True)
        with mp1, mp2, mp3, mp4, mp5:
            key_management.check_era5cli_config()
            with open(empty_path_era5, "r", encoding="utf-8") as f:
                assert f.readlines() == [
                    "url: https://www.github.com/\n",
                    "key: abc-def\n",
                ]

    def test_cdsrcfile_invalid_keys(self, empty_path_era5, valid_path_cds):
        """.cdsapirc exists. url+key is validated, and is bad."""
        mp1 = patch(
            "era5cli.key_management.attempt_cds_login",
            side_effect=key_management.InvalidLoginError,
        )
        mp2 = patch("era5cli.key_management.ERA5CLI_CONFIG_PATH", empty_path_era5)
        mp3 = patch("era5cli.key_management.CDSAPI_CONFIG_PATH", valid_path_cds)
        mp4 = patch("sys.stdin.isatty", return_value=True)
        with mp1, mp2, mp3, mp4:
            with pytest.raises(
                key_management.InvalidLoginError, match="No valid CDS login found"
            ):
                key_management.check_era5cli_config()


class TestAttemptCdsLogin:
    """Test the keymanagement.attempt_cds_login function.

    attempt_cds_login is monkeypatched elsewhere, these tests ensure it works as
    expected.
    """

    def test_status_fail(self):
        with patch("cdsapi.Client.status", side_effect=rex.ConnectionError):
            with pytest.raises(rex.ConnectionError, match="Failed to connect to CDS"):
                key_management.attempt_cds_login(url="test", key="abc:def")

    def test_connection_fail(self):
        mp1 = patch("cdsapi.Client.status")
        mp2 = patch(
            "cdsapi.Client.retrieve",
            side_effect=Exception("401"),
        )
        with mp1, mp2:
            with pytest.raises(
                key_management.InvalidLoginError,
                match="Authorization with the CDS served failed",
            ):
                key_management.attempt_cds_login(
                    url="https://www.github.com/", key="abc:def"
                )

    def test_retrieve_fail(self):
        mp1 = patch("cdsapi.Client.status")
        mp2 = patch(
            "cdsapi.Client.retrieve",
            side_effect=Exception("There is no data matching your request"),
        )
        with mp1, mp2:
            with pytest.raises(
                key_management.InvalidRequestError,
                match="Something changed in the CDS API",
            ):
                key_management.attempt_cds_login(url="test", key="abc:def")

    def test_all_pass(self):
        mp1 = patch("cdsapi.Client.status")
        mp2 = patch("cdsapi.Client.retrieve")
        with mp1, mp2:
            assert key_management.attempt_cds_login(url="test", key="abc:def") is True
