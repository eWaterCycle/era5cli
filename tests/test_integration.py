"""Tests to check the full era5cli workflow."""

import pytest

import era5cli.cli as cli


# geopotential needs '--levels surface' to be correctly interpreted
call1 = """era5cli hourly --variables geopotential --startyear 2008 --dryrun
--levels surface"""

result1 = """reanalysis-era5-single-levels {'variable': 'geopotential', 'year':
2008, 'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
'11', '12'], 'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
'06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
'14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
'22:00', '23:00'], 'format': 'netcdf', 'product_type': 'reanalysis', 'day':
['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
'14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
'27', '28', '29', '30', '31']} era5_geopotential_2008_hourly.nc"""

# orography is translated to geopotential in the query
call2 = """era5cli hourly --variables orography --startyear 2008 --dryrun"""

result2 = """reanalysis-era5-single-levels {'variable': 'geopotential', 'year':
2008, 'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
'11', '12'], 'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
'06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
'14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
'22:00', '23:00'], 'format': 'netcdf', 'product_type': 'reanalysis', 'day':
['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
'14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
'27', '28', '29', '30', '31']} era5_orography_2008_hourly.nc"""

# without --levels surface, geopotential calls pressure level data
call3 = """era5cli hourly --variables geopotential --startyear 2008 --dryrun"""

result3 = """reanalysis-era5-pressure-levels {'variable': 'geopotential',
'year': 2008, 'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09',
'10', '11', '12'], 'time': ['00:00', '01:00', '02:00', '03:00', '04:00',
'05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
'13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
'21:00', '22:00', '23:00'], 'format': 'netcdf', 'pressure_level': [1, 2, 3, 5,
7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450,
500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975,
1000], 'product_type': 'reanalysis', 'day': ['01', '02', '03', '04', '05',
'06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
'19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']}
era5_geopotential_2008_hourly.nc"""


call_result = [
    (call1, result1),
    (call2, result2),
    (call3, result3)
    ]
ids = [call[0] for call in call_result]


@pytest.mark.parametrize("call,result", call_result, ids=ids)
def test_main(call, result, capsys):
    call = call.split()
    # until the actual fetch is monkeypatched, make sure the tests are dryruns
    if '--dryrun' not in call:
        pytest.fail('call must be a dryrun')
    cli.main(call)
    captured = capsys.readouterr().out
    result = result.replace('\n', ' ')
    result = result + '\n'
    assert result == captured
