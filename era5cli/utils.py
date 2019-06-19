"""Utility functions."""


def zpadlist(values: list, inputtype: str, minval: int, maxval: int) -> list:
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


def zpad_days(values: list) -> list:
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
    return zpadlist(values, 'days', 1, 31)


def zpad_months(values: list) -> list:
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
    return zpadlist(values, 'months', 1, 12)


def format_hours(values: list) -> list:
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
