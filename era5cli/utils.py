"""Utility functions."""

import shutil
import prettytable
from netCDF4 import Dataset
from pathlib import Path

import era5cli
from era5cli.__version__ import __version__ as era5cliversion


def _zpadlist(values: list, inputtype: str, minval: int, maxval: int) -> list:
    """Return a list of zero padded strings and perform input checks.

    Returns a list of zero padded strings of day numbers from a list of
    input days. Invalid month numbers (e.g. outside of 1-31) will raise
    an exception.

    Parameters
    ----------
    values: list(int)
        List of integers that will be zero-padded.
    inputttype: str
        String identifying the input data used in error messages.
    minval: int
        Minimum value that all elements in `values` are checked against.
    maxval: int
        Maximum value that all elements in `values` are checked against.

    Returns
    -------
    list(str)
        List of zero-padded strings (e.g. ['01', '02',..., '31']).

    Raises
    ------
    AssertionError
        If any value in the list is not within `minval<=value<=maxval`.
    """
    returnlist = []
    for value in values:
        assert (int(value) >= minval), (
            'invalid value specified for {}: {}'.format(inputtype, value))
        assert (int(value) <= maxval), (
            'invalid value specified for {}: {}'.format(inputtype, value))
        returnlist += [str(int(value)).zfill(2)]
    return returnlist


def _zpad_days(values: list) -> list:
    """Return a list of zero padded strings.

    Returns a list of zero padded strings of day numbers from a list of
    input days. Invalid month numbers (e.g. outside of 1-31) will raise
    an exception.

    Parameters
    ----------
    values: list(int)
        List of month numbers (1-31).

    Returns
    -------
    list(str)
        List of zero-padded strings of months (e.g. ['01', '02',..., '31']).
    """
    return _zpadlist(values, 'days', 1, 31)


def _zpad_months(values: list) -> list:
    """Return a list of zero padded strings.

    Returns a list of zero padded strings of month numbers from a list of
    input months. Invalid month numbers (e.g. outside of 1-12) will raise
    an exception.

    Parameters
    ----------
    values: list(int)
        List of month numbers (1-12).

    Returns
    -------
    list(str)
        List of zero-padded strings of months (e.g. ['01', '02',..., '12']).
    """
    return _zpadlist(values, 'months', 1, 12)


def _format_hours(values: list) -> list:
    """Return a list of xx:00 formated time strings.

    Returns a list xx:00 formated time strings from a list of input hours.
    Invalid iput hours (e.g. outside of 0-23) will raise an exception.

    Parameters
    ----------
    values: list(int)
        List of month numbers (0-23).

    Returns
    -------
    list(str)
        List of xx:00 formatted time strings (e.g. ['00:00', '01:00', ...,
        '23:00']).
    """
    returnlist = []
    for value in values:
        assert (int(value) >= 0), (
            'invalid value specified for hours: {}'.format(value))
        assert (int(value) <= 23), (
            'invalid value specified for hours: {}'.format(value))
        returnlist += ["{}:00".format(str(value).zfill(2))]
    return returnlist


def _print_multicolumn(header: str, info: list):
    """Print a list of strings in several columns.

    Parameters
    ----------
    header: str
        Table header string.
    info: list()
        Data to be printed.
    """
    # get size of terminal window
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    # maximum width of string in list
    maxwidth = max([len(str(x)) for x in info])
    # calculate number of columns that fit on screen
    ncols = columns // (maxwidth + 2)
    # calculate number of rows
    nrows = - ((-len(info)) // ncols)
    # the number of columns may be reducible for that many rows.
    ncols = - ((-len(info)) // nrows)
    table = prettytable.PrettyTable([str(x) for x in range(ncols)])
    table.title = header
    table.header = False
    table.align = 'l'
    table.hrules = prettytable.NONE
    table.vrules = prettytable.NONE
    chunks = [info[i:i + nrows] for i in
              range(0, len(info), nrows)]
    chunks[-1].extend('' for i in range(nrows - len(chunks[-1])))
    chunks = zip(*chunks)
    for chunk in chunks:
        table.add_row(chunk)
    print(table)


def _append_history(fname):
    """Append era5cli version information.

    Parameters
    ----------
    fname: str
        Filename.
    """
    appendtxt = "Downloaded using {} {}.".format(era5cli.__name__,
                                                 era5cliversion)
    extension = Path(fname).suffix
    if extension == ".nc":
        _append_netcdf_history(fname, appendtxt)


def _append_netcdf_history(ncfile: str, appendtxt: str):
    """Append era5cli version and download command to netCDF history.

    Parameters
    ----------
    ncfile: str
        Filename of netCDF file.
    appendtxt: str
        Text to append to history of netCDF file.
    """
    # open netCDF file rw and append to history
    ncfile = Dataset(ncfile, 'r+')
    try:
        ncfile.history = "{}\n{}".format(appendtxt, ncfile.history)
    except AttributeError:
        ncfile.history = appendtxt
    ncfile.close()
