"""Tests to check the full era5cli workflow."""

import logging
from textwrap import dedent
from unittest import mock
import pytest
from era5cli.cli import main


@pytest.fixture(scope="module", autouse=True)
def my_thing_mock():
    with mock.patch(
        "era5cli.fetch.key_management.check_era5cli_config", autospec=True
    ) as _fixture:
        yield _fixture


# combine calls with result and possible warning message
call_result = [
    {
        # geopotential needs '--levels surface' to be correctly interpreted
        "call": dedent(
            """\
            era5cli hourly --variables geopotential --startyear 2008 --dryrun
             --splitmonths False --levels surface"""
        ),
        "result": dedent(
            """\
            reanalysis-era5-single-levels {'variable': 'geopotential', 'year':
            2008, 'month': ['01', '02', '03', '04', '05', '06', '07', '08',
            '09', '10', '11', '12'], 'time': ['00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00',
            '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00',
            '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
            'data_format': 'netcdf', 'download_format': 'unarchived',
            'product_type': 'reanalysis', 'day': ['01',
            '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
            '24', '25', '26', '27', '28', '29', '30', '31']}
            era5_geopotential_2008_hourly.nc"""
        ),
        "warn": "Getting variable from surface level data.",
    },
    {
        # without --levels surface, geopotential calls pressure level data
        # Note: only request a single month to avoid TooLargeRequest
        "call": dedent(
            """\
            era5cli hourly --variables geopotential --startyear 2008 --months 01
            --dryrun"""
        ),
        "result": dedent(
            """\
            reanalysis-era5-pressure-levels {'variable': 'geopotential',
            'year': 2008, 'month': '01', 'time': ['00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00',
            '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00',
            '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
            'data_format': 'netcdf', 'download_format': 'unarchived',
            'pressure_level': [1, 2, 3, 5, 7, 10, 20, 30,
            50, 70, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500,
            550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950,
            975, 1000], 'product_type': 'reanalysis', 'day': ['01', '02', '03',
            '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
            '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
            '26', '27', '28', '29', '30', '31']}
            era5_geopotential_2008-01_hourly.nc"""
        ),
        "warn": "Getting variable from pressure level data.",
    },
    {
        # era5-Land is combined with monthly means
        "call": dedent(
            """\
            era5cli monthly --variables snow_cover --startyear 2008 --land
            --dryrun"""
        ),
        "result": dedent(
            """\
            reanalysis-era5-land-monthly-means {'variable': 'snow_cover',
            'year': 2008, 'month': ['01', '02', '03', '04', '05', '06', '07',
            '08', '09', '10', '11', '12'], 'time': ['00:00'], 'data_format': 'netcdf',
            'download_format': 'unarchived',
            'product_type': 'monthly_averaged_reanalysis'}
            era5-land_snow_cover_2008_monthly.nc"""
        ),
    },
]


def clean_ids(call):
    call = call.replace("\n", " ")
    call = call.replace("--dryrun", "")
    return call


ids = [clean_ids(item["call"]) for item in call_result]


@pytest.mark.parametrize("call_result", call_result, ids=ids)
def test_main(call_result, capsys, caplog):
    call = call_result["call"].split()
    result = call_result["result"].replace("\n", " ") + "\n"
    # until the actual fetch is monkeypatched, make sure the tests are dryruns
    if "--dryrun" not in call:
        pytest.fail("call must be a dryrun")
    with caplog.at_level(logging.INFO):
        with mock.patch(
            "era5cli.fetch.key_management.load_era5cli_config",
            return_value=("url", "key"),
        ):
            main(call)
    captured = capsys.readouterr().out
    assert result in captured
    try:
        warn = call_result["warn"]
        assert warn in caplog.text
    except KeyError:
        assert caplog.text == ""
