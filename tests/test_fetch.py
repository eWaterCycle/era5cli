"""Tests for era5cli Fetch class."""

from era5cli import fetch
import pytest
import unittest.mock as mock


def initialize(outputformat='netcdf', merge=False, statistics=None,
               synoptic=None, ensemble=True, pressurelevels=None,
               threads=2, period='hourly', variables=['total_precipitation'],
               years=[2008, 2009], months=list(range(1, 13)),
               days=list(range(1, 32)), hours=list(range(0, 24)),
               prelimbe=False, land=False):
    """Initializer of the class."""
    era5 = fetch.Fetch(years=years,
                       months=months,
                       days=days,
                       hours=hours,
                       variables=variables,
                       outputformat=outputformat,
                       outputprefix='era5',
                       period=period,
                       ensemble=ensemble,
                       statistics=statistics,
                       synoptic=synoptic,
                       pressurelevels=pressurelevels,
                       merge=merge,
                       threads=threads,
                       prelimbe=prelimbe,
                       land=land)
    return era5


def test_init():
    """Test init function of Fetch class."""
    era5 = fetch.Fetch(years=[2008, 2009],
                       months=list(range(1, 13)),
                       days=list(range(1, 32)),
                       hours=list(range(0, 24)),
                       variables=['total_precipitation'],
                       outputformat='netcdf',
                       outputprefix='era5',
                       period='hourly',
                       ensemble=True,
                       statistics=None,
                       synoptic=None,
                       pressurelevels=None,
                       merge=False,
                       threads=2,
                       prelimbe=False)

    valid_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12']
    assert era5.months == valid_months

    valid_days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                  '31']
    assert era5.days == valid_days

    valid_hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                   '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                   '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                   '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    assert era5.hours == valid_hours

    assert era5.variables == ['total_precipitation']
    assert era5.outputformat == 'netcdf'
    assert era5.outputprefix == 'era5'
    assert era5.period == 'hourly'
    assert era5.ensemble
    assert era5.statistics is None
    assert era5.synoptic is None
    assert era5.pressure_levels is None
    assert not era5.merge
    assert era5.threads == 2
    assert not era5.prelimbe
    assert not era5.land

    # initializing hourly variable with days=None should result in ValueError
    with pytest.raises(TypeError):
        era5 = initialize(variables=['temperature'],
                          period='hourly',
                          days=None)

    # initializing monthly variable with days=None returns fetch.Fetch object
    era5 = initialize(variables=['temperature'],
                      period='monthly',
                      days=None)
    assert isinstance(era5, fetch.Fetch)


@mock.patch("cdsapi.Client", autospec=True)
@mock.patch("era5cli.utils._append_history", autospec=True)
def test_fetch_nodryrun(cds, era5cli_utils_append_history):
    """Test fetch function of Fetch class."""
    era5 = initialize()
    assert era5.fetch() is None

    era5 = initialize(outputformat='grib', merge=True)
    assert era5.fetch() is None

    era5 = initialize(outputformat='grib', merge=True,
                      threads=None)
    assert era5.fetch() is None

    era5 = initialize(outputformat='grib', merge=True,
                      threads=None, ensemble=True, statistics=True)
    assert era5.fetch() is None

    era5 = initialize(outputformat='grib', merge=True,
                      threads=None, pressurelevels=[1, 2],
                      variables=['temperature'])
    assert era5.fetch() is None

    era5 = initialize(outputformat='grib', merge=True,
                      threads=None, pressurelevels=[1, 2],
                      variables=['temperature'],
                      period='monthly')
    assert era5.fetch() is None

    # invalid pressure level should raise ValueError
    era5 = initialize(outputformat='grib', merge=True,
                      threads=None, pressurelevels=[1, 2, 9],
                      variables=['temperature'])
    with pytest.raises(ValueError):
        assert era5.fetch()

    # invalid variable name should raise ValueError
    era5 = initialize(outputformat='grib', merge=True,
                      threads=None,
                      variables=['unknown'])
    with pytest.raises(ValueError):
        assert era5.fetch()

    # check check against monthly unavailable data raise ValueError
    era5 = initialize(outputformat='grib', merge=True,
                      threads=None,
                      variables=['wave_spectral_skewness'],
                      period='monthly')
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
    assert era5.ext == 'nc'

    era5 = initialize(outputformat='netcdf')
    era5._extension()
    assert era5.ext == 'nc'

    # checking grib outputformat
    era5 = initialize(outputformat='grib', merge=True)
    era5._extension()
    assert era5.ext == 'grb'

    #  unkown outputformat should raise a ValueError
    era5 = initialize(outputformat='unknown', merge=True)
    with pytest.raises(ValueError):
        assert era5._extension()


def test_define_outputfilename():
    """Test _define_outputfilename function of Fetch class."""
    era5 = initialize()
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', [2008])
    assert fname == 'era5_total_precipitation_2008_hourly_ensemble.nc'

    era5 = initialize(outputformat='grib', merge=True)
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', era5.years)
    assert fname == 'era5_total_precipitation_2008-2009_hourly_ensemble.grb'

    era5 = initialize(outputformat='grib', merge=True, statistics=True)
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', era5.years)
    fn = 'era5_total_precipitation_2008-2009_hourly_ensemble_statistics.grb'
    assert fname == fn

    era5 = initialize(outputformat='grib', merge=True, synoptic=True)
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', era5.years)
    fn = 'era5_total_precipitation_2008-2009_hourly_ensemble_synoptic.grb'
    assert fname == fn

    era5 = initialize(land=True, ensemble=False)
    era5._extension()
    fname = era5._define_outputfilename('total_precipitation', [2008])
    fn = 'era5-land_total_precipitation_2008_hourly.nc'
    assert fname == fn


def test_number_outputfiles(capsys):
    """Test function for the number of outputs."""
    # two variables and three years
    era5 = initialize(variables=['total_precipitation', 'runoff'],
                      years=[2007, 2008, 2009], merge=False)
    era5.fetch(dryrun=True)
    captured = capsys.readouterr()
    outputlength = len(captured.out.split('\n')) - 1
    if not era5.merge:
        # No. of outputs is 2*3 = 6 if merge = False
        assert outputlength == len(era5.years) * len(era5.variables)
    else:
        # No. of outputs is 2*1 = 2 if merge = True
        assert outputlength == len(era5.variables)

    # one variable and three years
    era5 = initialize(variables=['total_precipitation'],
                      years=[2007, 2008, 2009], merge=False)
    era5.fetch(dryrun=True)
    captured = capsys.readouterr()
    outputlength = len(captured.out.split('\n')) - 1
    if not era5.merge:
        # No. of outputs is 1*3 = 3 if merge = False
        assert outputlength == len(era5.years) * len(era5.variables)
    else:
        # No. of outputs is 1 if merge = True
        assert outputlength == len(era5.variables)

    # two variables and one year
    era5 = initialize(variables=['total_precipitation', 'runoff'],
                      years=[2007], merge=False)
    era5.fetch(dryrun=True)
    captured = capsys.readouterr()
    outputlength = len(captured.out.split('\n')) - 1
    if not era5.merge:
        # No. of outputs is 2*1 = 2 if merge = False
        assert outputlength == len(era5.years) * len(era5.variables)
    else:
        # No. of outputs is 2 if merge = True
        assert outputlength == len(era5.variables)
    del era5, captured


def test_product_type():
    """Test _product_type function of Fetch class."""
    # Default hourly data
    era5 = initialize()
    producttype = era5._product_type()
    assert producttype == 'ensemble_members'

    era5.statistics = True
    producttype = era5._product_type()
    assert producttype == [
        'ensemble_members', 'ensemble_mean', 'ensemble_spread'
    ]

    era5.ensemble = False  # statistics will be ignored
    producttype = era5._product_type()
    assert producttype == 'reanalysis'

    # Default monthly data
    era5.period = 'monthly'
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis'

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis_by_hour_of_day'

    era5.ensemble = True
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_ensemble_members_by_hour_of_day'

    era5.synoptic = False
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_ensemble_members'

    # Preliminary back extension monthly data have different names
    era5.prelimbe = True
    producttype = era5._product_type()
    assert producttype == 'members-monthly-means-of-daily-means'

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == 'members-synoptic-monthly-means'

    era5.ensemble = False
    producttype = era5._product_type()
    assert producttype == 'reanalysis-synoptic-monthly-means'

    era5.synoptic = False
    producttype = era5._product_type()
    assert producttype == 'reanalysis-monthly-means-of-daily-means'

    # ERA5 land has more limited options
    era5.land = True
    era5.prelimbe = False
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis'

    era5.synoptic = True
    producttype = era5._product_type()
    assert producttype == 'monthly_averaged_reanalysis_by_hour_of_day'

    era5.period = 'hourly'
    producttype = era5._product_type()
    assert producttype is None


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
    missing_monthly_var = "altimeter_wave_height"

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
    era5.land = False
    era5._check_variable(missing_monthly_var)

    # Missing monthly vars should fail if period is monthly
    era5.period = 'monthly'
    with pytest.raises(ValueError):
        era5._check_variable(missing_monthly_var)


def test_build_name():
    """Test _build_name function of Fetch class."""
    era5 = initialize()

    name = era5._build_name('total_precipitation')
    assert name == "reanalysis-era5-single-levels"

    name = era5._build_name('temperature')
    assert name == "reanalysis-era5-pressure-levels"

    era5.period = "monthly"
    name = era5._build_name('temperature')
    assert name == "reanalysis-era5-pressure-levels-monthly-means"

    name = era5._build_name('total_precipitation')
    assert name == "reanalysis-era5-single-levels-monthly-means"

    # Test names for back extension
    era5.prelimbe = True
    name = era5._build_name('temperature')
    assert name == ("reanalysis-era5-pressure-levels-monthly-means"
                    "-preliminary-back-extension")

    name = era5._build_name('total_precipitation')
    assert name == ("reanalysis-era5-single-levels-monthly-means"
                    "-preliminary-back-extension")

    era5.period = "hourly"
    name = era5._build_name('temperature')
    assert name == "reanalysis-era5-pressure-levels-preliminary-back-extension"

    name = era5._build_name('total_precipitation')
    assert name == "reanalysis-era5-single-levels-preliminary-back-extension"

    # Tests for era5 land
    era5.prelimbe = False
    with pytest.raises(ValueError):
        era5._build_name('snow_cover')

    era5.land = True
    name = era5._build_name('snow_cover')
    assert name == "reanalysis-era5-land"

    era5.period = "monthly"
    name = era5._build_name('snow_cover')
    assert name == "reanalysis-era5-land-monthly-means"


def test_build_request():
    """Test _build_request function of Fetch class."""
    # hourly data
    era5 = initialize(period='hourly',
                      variables=['total_precipitation'],
                      years=[2008])
    (name, request) = era5._build_request('total_precipitation', [2008])
    assert name == 'reanalysis-era5-single-levels'
    req = {'variable': 'total_precipitation', 'year': [2008],
           'product_type': 'ensemble_members',
           'month': ['01', '02', '03', '04', '05', '06',
                     '07', '08', '09', '10', '11', '12'],
           'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09',
                   '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', '23', '24', '25', '26', '27',
                   '28', '29', '30', '31'],
           'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
           'format': 'netcdf'}
    assert request == req

    # monthly data
    era5 = initialize(period='monthly',
                      variables=['total_precipitation'],
                      years=[2008])
    (name, request) = era5._build_request('total_precipitation', [2008])
    assert name == 'reanalysis-era5-single-levels-monthly-means'
    req = {'variable': 'total_precipitation', 'year': [2008],
           'product_type': 'monthly_averaged_ensemble_members',
           'month': ['01', '02', '03', '04', '05', '06',
                     '07', '08', '09', '10', '11', '12'],
           'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
           'format': 'netcdf'}
    assert request == req

    # preliminary back extension
    era5 = initialize(period='monthly',
                      variables=['total_precipitation'],
                      years=[1970],
                      prelimbe=True)
    (name, request) = era5._build_request('total_precipitation', [1970])
    print(request)
    assert name == (
        "reanalysis-era5-single-levels-monthly"
        "-means-preliminary-back-extension"
    )
    req = {'variable': 'total_precipitation', 'year': [1970],
           'product_type': 'members-monthly-means-of-daily-means',
           'month': ['01', '02', '03', '04', '05', '06',
                     '07', '08', '09', '10', '11', '12'],
           'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
           'format': 'netcdf'}
    assert request == req

    # land
    era5 = initialize(period='monthly',
                      variables=['snow_cover'],
                      hours=[0],
                      land=True,
                      ensemble=False)

    (name, request) = era5._build_request('snow_cover', [2008])
    assert name == (
        "reanalysis-era5-land-monthly-means"
    )
    req = {'variable': 'snow_cover', 'year': [2008],
           'product_type': 'monthly_averaged_reanalysis',
           'month': ['01', '02', '03', '04', '05', '06',
                     '07', '08', '09', '10', '11', '12'],
           'time': ['00:00'],
           'format': 'netcdf'}
    assert request == req

    # requesting 3d variable with pressurelevels=None should give a ValueError
    era5 = initialize(variables=['temperature'], pressurelevels=None)
    with pytest.raises(ValueError):
        assert era5._build_request('temperature', [2008])


def test_incompatible_options():
    """Test that invalid combinations of arguments don't silently pass."""
    era5 = initialize(land=True, prelimbe=True)
    with pytest.raises(ValueError):
        era5._build_request('total_precipitation', [2008])

    era5 = initialize(land=False)
    with pytest.raises(ValueError):
        era5._build_request('snow_cover', [2008])


@pytest.mark.xfail(reason='https://github.com/eWaterCycle/era5cli/issues/68')
def test_more_incompatible_options():
    era5 = initialize(land=True, ensemble=True)
    with pytest.raises(ValueError):
        era5._build_request('total_precipitation', [2008])

    era5 = initialize(statistics=True, ensemble=False)
    with pytest.raises(ValueError):
        era5._build_request('total_precipitation', [2008])
