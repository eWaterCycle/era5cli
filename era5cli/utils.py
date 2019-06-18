"""Utility functions."""

import prettytable
import shutil


def print_multicolumn(inputlist, header):
    """Print a list of strings in several columns."""
    # calculate number of rows needed
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    maxwidth = max([len(x) for x in inputlist])
    # calculate number of columns that fit on screen
    ncols = columns // (maxwidth + 2)
    # calculate number of rows
    nrows = - ((-len(inputlist)) // ncols)
    # the number of columns may be reducible for that many rows.
    ncols = - ((-len(inputlist)) // nrows)
    t = prettytable.PrettyTable([str(x) for x in range(ncols)])
    t.title = header
    t.header = False
    t.align = 'l'
    t.hrules = prettytable.NONE
    t.vrules = prettytable.NONE
    chunks = [inputlist[i:i + nrows] for i in range(0, len(inputlist), nrows)]
    chunks[-1].extend('' for i in range(nrows - len(chunks[-1])))
    chunks = zip(*chunks)
    for c in chunks:
        t.add_row(c)
    print(t)
