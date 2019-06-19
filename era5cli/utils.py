"""Utility functions."""


def zpadlist(values: list, inputtype: str, minval: int, maxval: int) -> list:
    """Return zero padded string and perform input checks."""
    returnlist = []
    for value in values:
        assert (int(value) >= minval), (
            'invalid value specified for {}: {}'.format(inputtype, value))
        assert (int(value) <= maxval), (
            'invalid value specified for {}: {}'.format(inputtype, value))
        returnlist += [str(int(value)).zfill(2)]
    return returnlist


def zpad_days(values: list) -> list:
    """Return zero padded string."""
    return zpadlist(values, 'days', 1, 31)


def zpad_months(values: list) -> list:
    """Return zero padded string."""
    return zpadlist(values, 'months', 1, 12)


def format_hours(values: list) -> list:
    """Return xx:00 formated time string."""
    returnlist = []
    for value in values:
        assert (int(value) >= 0), (
            'invalid value specified for hours: {}'.format(value))
        assert (int(value) <= 23), (
            'invalid value specified for hours: {}'.format(value))
        returnlist += ["{}:00".format(str(value).zfill(2))]
    return returnlist
