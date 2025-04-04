"""Tests for era5cli Fetch class."""

import pathlib
import unittest.mock as mock
import pytest
from era5cli import _request_size
from era5cli import fetch


# fmt: off
ALL_HOURS = [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
    "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
]

ALL_DAYS = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
    "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26",
    "27", "28", "29", "30", "31",
]

ALL_MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
# fmt: on


@pytest.fixture(scope="module", autouse=True)
def my_thing_mock():
    with mock.patch(
        "era5cli.fetch.key_management.check_era5cli_config", autospec=True
    ) as _fixture:
        yield _fixture


def initialize(
    outputformat="netcdf",
    merge=False,
    statistics=None,
    synoptic=None,
    ensemble=True,
    pressurelevels=None,
    threads=2,
    period="hourly",
    area=None,
    variables=["total_precipitation"],
    years=[2008, 2009],
    months=list(range(1, 13)),
    days=list(range(1, 32)),
    hours=list(range(24)),
    land=False,
    splitmonths=True,
    overwrite=False,
):
    with mock.patch(
        "era5cli.fetch.key_management.load_era5cli_config",
        return_value=("url", "key:uid"),
    ):
        """Initializer of the class."""
        return fetch.Fetch(
            years=years,
            months=months,
            days=days,
            hours=hours,
            area=area,
            variables=variables,
            outputformat=outputformat,
            outputprefix="era5",
            period=period,
            ensemble=ensemble,
            statistics=statistics,
            synoptic=synoptic,
            pressurelevels=pressurelevels,
            merge=merge,
            threads=threads,
            land=land,
            splitmonths=splitmonths,
            overwrite=overwrite,
        )


@mock.patch(
    "era5cli.fetch.key_management.load_era5cli_config", return_value=("url", "key:uid")
)
def test_init(mockpatch):
    """Test init function of Fetch class."""
    era5 = fetch.Fetch(
        years=[2008, 2009],
        months=list(range(1, 13)),
        days=list(range(1, 32)),
        hours=list(range(24)),
        variables=["total_precipitation"],
        outputformat="netcdf",
        outputprefix="era5",
        period="hourly",
        ensemble=True,
        statistics=None,
        synoptic=None,
        pressurelevels="surface",
        merge=False,
        threads=2,
    )

    assert era5.months == ALL_MONTHS
    assert era5.days == ALL_DAYS
    assert era5.hours == ALL_HOURS

    assert era5.variables == ["total_precipitation"]
    assert era5.outputformat == "netcdf"
    assert era5.outputprefix == "era5"
    assert era5.period == "hourly"
    assert era5.ensemble
    assert era5.statistics is None
    assert era5.synoptic is None
    assert era5.pressure_levels == "surface"
    assert not era5.merge
    assert era5.threads == 2
    assert not era5.land

    # initializing hourly variable with days=None should result in ValueError
    with pytest.raises(TypeError):
        era5 = initialize(
            variables=["temperature"], period="hourly", days=None, pressurelevels=[1]
        )

    # initializing monthly variable with days=None returns fetch.Fetch object
    era5 = initialize(
        variables=["temperature"], period="monthly", days=None, pressurelevels=[1]
    )
    assert isinstance(era5, fetch.Fetch)

    with pytest.raises(_request_size.TooLargeRequestError):
        initialize(
            land=True, variables=["skin_temperature"], ensemble=False, splitmonths=False
        )


@mock.patch("cdsapi.Client", autospec=True)
@mock.patch("era5cli.utils.append_history", autospec=True)
def test_fetch_nodryrun(cds, era5cli_utilsappend_history):
    """Test fetch function of Fetch class."""
    era5 = initialize()
    assert era5.fetch() is None

    era5 = initialize(outputformat="grib", merge=True)
    assert era5.fetch() is None

    era5 = initialize(outputformat="grib", merge=True, threads=None)
    assert era5.fetch() is None

    era5 = initialize(
        outputformat="grib", merge=True, threads=None, ensemble=True, statistics=True
    )
    assert era5.fetch() is None

    era5 = initialize(
        outputformat="grib",
        merge=True,
        threads=None,
        pressurelevels=[1, 2],
        variables=["temperature"],
    )
    assert era5.fetch() is None

    era5 = initialize(
        outputformat="grib",
        merge=True,
        threads=None,
        pressurelevels=[1, 2],
        variables=["temperature"],
        period="monthly",
    )
    assert era5.fetch() is None

    # invalid pressure level should raise ValueError
    with pytest.raises(ValueError):
        era5 = initialize(
            outputformat="grib",
            merge=True,
            threads=None,
            pressurelevels=[1, 2, 9],
            variables=["temperature"],
        )

    # invalid variable name should raise ValueError
    era5 = initialize(
        outputformat="grib", merge=True, threads=None, variables=["unknown"]
    )
    with pytest.raises(ValueError):
        assert era5.fetch()

    # check check against monthly unavailable data raise ValueError
    era5 = initialize(
        outputformat="grib",
        merge=True,
        threads=None,
        variables=["10m_wind_gust_since_previous_post_processing"],
        period="monthly",
    )
    with pytest.raises(ValueError):
        assert era5.fetch()


def test_fetch_dryrun():
    """Test fetch function of Fetch class with dryrun=False."""
    era5 = initialize()
    assert era5.fetch(dryrun=True) is None


def test_extension():
    """Test _extension function of Fetch class."""
    # checking netcdf outputformat
    era5 = initialize()
    era5._extension()
    assert era5.ext == "nc"

    era5 = initialize(outputformat="netcdf")
    era5._extension()
    assert era5.ext == "nc"

    # checking grib outputformat
    era5 = initialize(outputformat="grib", merge=True)
    era5._extension()
    assert era5.ext == "grb"

    #  unkown outputformat should raise a ValueError
    era5 = initialize(outputformat="unknown", merge=True)
    with pytest.raises(ValueError):
        assert era5._extension()


def test_define_outputfilename():
    """Test _define_outputfilename function of Fetch class."""
    era5 = initialize()
    era5._extension()
    fname = era5._define_outputfilename("total_precipitation", [2008])
    assert fname == "era5_total_precipitation_2008_hourly_ensemble.nc"

    era5 = initialize(outputformat="grib", merge=True)
    era5._extension()
    fname = era5._define_outputfilename("total_precipitation", era5.years)
    assert fname == "era5_total_precipitation_2008-2009_hourly_ensemble.grb"

    era5 = initialize(outputformat="grib", merge=True, statistics=True)
    era5._extension()
    fname = era5._define_outputfilename("total_precipitation", era5.years)
    fn = "era5_total_precipitation_2008-2009_hourly_ensemble_statistics.grb"
    assert fname == fn

    era5 = initialize(outputformat="grib", merge=True, synoptic=True)
    era5._extension()
    fname = era5._define_outputfilename("total_precipitation", era5.years)
    fn = "era5_total_precipitation_2008-2009_hourly_ensemble_synoptic.grb"
    assert fname == fn

    era5 = initialize(land=True, ensemble=False, splitmonths=True)
    era5._extension()
    fname = era5._define_outputfilename("total_precipitation", [2008], month="01")
    fn = "era5-land_total_precipitation_2008-01_hourly.nc"
    assert fname == fn

    era5.area = [90.0, -180.0, -90.0, 180.0]
    fname = era5._define_outputfilename("total_precipitation", [2008], month="01")
    fn = "era5-land_total_precipitation_2008-01_hourly_180W-180E_90S-90N.nc"
    assert fname == fn

    era5.area = [90.0, -180.0, -80.999, 170.001]
    fname = era5._define_outputfilename("total_precipitation", [2008], month="01")
    fn = "era5-land_total_precipitation_2008-01_hourly_180W-170E_81S-90N.nc"
    assert fname == fn

    era5.area = [0, 120, -90, 180]
    fname = era5._define_outputfilename("total_precipitation", [2008], month="01")
    fn = "era5-land_total_precipitation_2008-01_hourly_120E-180E_90S-0N.nc"
    assert fname == fn


_vars = ["total_precipitation", "runoff"]
_years = [2007, 2008, 2009]


@pytest.mark.parametrize(
    "variables, years, merge, ensemble, splitmonths, expected",
    [
        (_vars, _years, False, False, False, 2 * 3),
        (_vars, _years, True, False, False, 2),  # test merge
        (_vars, _years, False, True, False, 2 * 3),  # old default
        (_vars, _years, False, True, True, 2 * 3 * 12),  # future default
        (_vars, _years[:1], False, False, False, 2 * 1),
        (_vars[:1], _years, False, False, False, 1 * 3),
    ],
)
def test_number_outputfiles(
    capsys, variables, years, merge, ensemble, splitmonths, expected
):
    """Test function for the number of outputs."""
    # two variables and three years
    era5 = initialize(
        variables=variables,
        years=years,
        merge=merge,
        ensemble=ensemble,
        splitmonths=splitmonths,
    )
    era5.fetch(dryrun=True)
    captured = capsys.readouterr()

    # Every request has 'product_type' in it once, ie. the number of requests equals:
    nrequests = captured.out.count("product_type")
    assert nrequests == expected


def test_product_type():
    """Test _product_type function of Fetch class."""
    # Default hourly data
    era5 = initialize()
    producttype = era5._product_type()
    assert producttype == "ensemble_members"

    era5.statistics = True
    producttype = era5._product_type()
    assert producttype == ["ensemble_members", "ensemble_mean", "ensemble_spread"]

    era5.ensemble = False  # statistics will be ignored
    producttype = era5._product_type()
    assert producttype == "reanalysis"

    # Default monthly data
    era5.period = "monthly"
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_reanalysis"

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_reanalysis_by_hour_of_day"

    era5.ensemble = True
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_ensemble_members_by_hour_of_day"

    era5.synoptic = False
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_ensemble_members"

    # ERA5 land has more limited options
    era5.land = True
    era5.ensemble = False
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_reanalysis"

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == "monthly_averaged_reanalysis_by_hour_of_day"

    era5.period = "hourly"
    producttype = era5._product_type()
    assert producttype is None

    era5.ensemble = True
    with pytest.raises(AssertionError):
        producttype = era5._product_type()


def test_check_levels():
    """Test _check_levels function of Fetch class"""
    era5 = initialize()
    era5.variables = "temperature"

    # No levels should raise
    with pytest.raises(ValueError):
        era5._check_levels()

    # Valid levels should pass
    era5.pressure_levels = [1000, 950]
    era5._check_levels()

    # Invalid levels should raise
    era5.pressure_levels = [777]
    with pytest.raises(ValueError):
        era5._check_levels()


def test_check_variable():
    """Test _check_variable function of Fetch class."""
    era5 = initialize()

    land_only_variable = "snow_cover"
    slev_only_variable = "vertical_integral_of_mass_tendency"
    missing_monthly_var = "10m_wind_gust_since_previous_post_processing"

    # Invalid variables should raise
    with pytest.raises(ValueError):
        era5._check_variable("invalid_precipitation")

    # Valid variable with invalid dataset option should raise
    with pytest.raises(ValueError):
        era5._check_variable(land_only_variable)

    # But with the right dataset option it should pass
    era5.land = True
    era5._check_variable(land_only_variable)

    # And variables incompatible with ERA5 land should fail
    with pytest.raises(ValueError):
        era5._check_variable(slev_only_variable)

    # Missing monthly vars should pass if period is hourly
    era5.period = "hourly"
    era5.land = False
    era5._check_variable(missing_monthly_var)

    # Missing monthly vars should fail if period is monthly
    era5.period = "monthly"
    with pytest.raises(ValueError):
        era5._check_variable(missing_monthly_var)


def test_build_name():
    """Test _build_name function of Fetch class."""
    era5 = initialize()

    name = era5._build_name("total_precipitation")[0]
    assert name == "reanalysis-era5-single-levels"

    name = era5._build_name("temperature")[0]
    assert name == "reanalysis-era5-pressure-levels"

    era5.period = "monthly"
    name = era5._build_name("temperature")[0]
    assert name == "reanalysis-era5-pressure-levels-monthly-means"

    name = era5._build_name("total_precipitation")[0]
    assert name == "reanalysis-era5-single-levels-monthly-means"

    # Tests for era5 land
    era5.period = "hourly"
    with pytest.raises(ValueError):
        era5._build_name("snow_cover")

    era5.land = True
    name = era5._build_name("snow_cover")[0]
    assert name == "reanalysis-era5-land"

    era5.period = "monthly"
    name = era5._build_name("snow_cover")[0]
    assert name == "reanalysis-era5-land-monthly-means"

    era5 = initialize()
    name = era5._build_name("geopotential")[0]
    assert name == "reanalysis-era5-pressure-levels"

    era5 = initialize()
    era5.pressure_levels = ["surface"]
    name = era5._build_name("geopotential")[0]
    assert name == "reanalysis-era5-single-levels"


def test_build_request():
    """Test _build_request function of Fetch class."""
    # hourly data
    era5 = initialize(
        period="hourly",
        variables=["total_precipitation"],
        years=[2008],
        splitmonths=False,
    )
    (name, request) = era5._build_request("total_precipitation", [2008])
    assert name == "reanalysis-era5-single-levels"
    req = {
        "variable": "total_precipitation",
        "year": [2008],
        "product_type": "ensemble_members",
        "month": ALL_MONTHS,
        "day": ALL_DAYS,
        "time": ALL_HOURS,
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    assert request == req

    # monthly data
    era5 = initialize(period="monthly", variables=["total_precipitation"], years=[2008])
    (name, request) = era5._build_request("total_precipitation", [2008])
    assert name == "reanalysis-era5-single-levels-monthly-means"
    req = {
        "variable": "total_precipitation",
        "year": [2008],
        "product_type": "monthly_averaged_ensemble_members",
        "month": ALL_MONTHS,
        "time": ALL_HOURS,
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    assert request == req

    # land
    era5 = initialize(
        period="monthly", variables=["snow_cover"], hours=[0], land=True, ensemble=False
    )

    (name, request) = era5._build_request("snow_cover", [2008])
    assert name == ("reanalysis-era5-land-monthly-means")
    req = {
        "variable": "snow_cover",
        "year": [2008],
        "product_type": "monthly_averaged_reanalysis",
        "month": ALL_MONTHS,
        "time": ["00:00"],
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    assert request == req

    # requesting 3d variable with pressurelevels=None should give a ValueError
    with pytest.raises(ValueError):
        era5 = initialize(variables=["temperature"], pressurelevels=None)


def test_incompatible_options():
    """Test that invalid combinations of arguments don't silently pass."""
    era5 = initialize(land=False)
    with pytest.raises(ValueError):
        era5._build_request("snow_cover", [2008])


@pytest.mark.xfail(reason="https://github.com/eWaterCycle/era5cli/issues/68")
def test_more_incompatible_options():
    era5 = initialize(land=True, ensemble=True)
    with pytest.raises(ValueError):
        era5._build_request("total_precipitation", [2008])

    era5 = initialize(statistics=True, ensemble=False)
    with pytest.raises(ValueError):
        era5._build_request("total_precipitation", [2008])


def test_area():
    """Test that area is parsed properly."""
    era5 = initialize()
    assert era5.area is None

    era5 = initialize(area=[90, -180, -90, 180])
    (name, request) = era5._build_request("total_precipitation", [2008])
    assert era5.area == [90, -180, -90, 180]
    assert request["area"] == [90, -180, -90, 180]

    # Decimals are rounded down
    era5 = initialize(area=[89.9999, -179.90, -90.0000, 179.012])
    (name, request) = era5._build_request("total_precipitation", [2008])
    assert request["area"] == [90.0, -179.90, -90.0, 179.01]

    # lat_max may not be lower than lat_min
    with pytest.raises(ValueError):
        era5 = initialize(area=[-10, -180, 10, 180])
        era5._build_request("total_precipitation", [2008])

    # lon_min higher than lon_max should be ok
    era5 = initialize(area=[90, 120, -90, -120])
    (name, request) = era5._build_request("total_precipitation", [2008])
    assert request["area"] == [90.0, 120.0, -90.0, -120.0]

    # lat_max may not equal lat_min
    with pytest.raises(ValueError):
        era5 = initialize(area=[0, -180, 0, 180])
        era5._build_request("total_precipitation", [2008])

    # lon_min may not equal lon_max
    with pytest.raises(ValueError):
        era5 = initialize(area=[90, 0, -90, 0])
        era5._build_request("total_precipitation", [2008])

    # lat_max, lon_min, lat_min, lon_max may not be out of bounds
    with pytest.raises(ValueError):
        era5 = initialize(area=[1000, -180, -90, 180])
        era5._build_request("total_precipitation", [2008])
    with pytest.raises(ValueError):
        era5 = initialize(area=[90, 1000, -90, 180])
        era5._build_request("total_precipitation", [2008])
    with pytest.raises(ValueError):
        era5 = initialize(area=[90, -180, 1000, 180])
        era5._build_request("total_precipitation", [2008])
    with pytest.raises(ValueError):
        era5 = initialize(area=[90, -180, -90, 1000])
        era5._build_request("total_precipitation", [2008])

    # Coordinate missing
    with pytest.raises(ValueError):
        era5 = initialize(area=[-180, 180, -90])
        era5._build_request("total_precipitation", [2008])


def test_file_exists():
    with mock.patch.object(pathlib.Path, "exists", return_value=True):
        era5 = initialize()

        mp_yes = mock.patch("builtins.input", return_value="Y")
        mp_no = mock.patch("builtins.input", return_value="N")
        mp_atty = mock.patch("sys.stdin.isatty", return_value=True)
        with mp_yes, mp_atty:
            era5.fetch(dryrun=True)

        with mp_no, mp_atty:
            with pytest.raises(FileExistsError):
                era5.fetch(dryrun=True)

        # Last one should have isatty->False.
        with pytest.raises(FileExistsError):
            era5.fetch(dryrun=True)


def test_overwrite():
    with mock.patch.object(pathlib.Path, "exists", return_value=True):
        era5 = initialize(overwrite=True)
        era5.fetch(dryrun=True)
