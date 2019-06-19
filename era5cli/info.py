"""Print ERA5 information on available variables and levels."""

import prettytable
import shutil
import era5cli.inputref as ref


class Info:
    """Print ERA5 information on available variables and levels.

    Parameters
    ----------
        infotype: str
            Type of information that needs to be printed. Supported are
            'levels', '2Dvars', and '3Dvars'.

    Raises
    ------
    KeyError
        If `infotype` is not any of ['levels', '2Dvars', '3Dvars'].

    """

    def __init__(self, infotype: str):
        """Initialization of Info class.

        Parameters
        ----------
            infotype: str
                Type of information that needs to be printed. Supported are
                'levels', '2Dvars', and '3Dvars'.

        Raises
        ------
        KeyError
            If `infotype` is not any of ['levels', '2Dvars', '3Dvars'].
        """
        self.infotype = infotype
        """str: Type of information that needs to be printed."""
        try:
            self.infolist = ref.refdict[self.infotype]
            """list: List with information to be printed."""
        except KeyError:
            raise Exception('Unknown value for reference argument.')

    def list(self):
        """Print a list of available variables or pressure levels.

        Prints a list of available variables or pressure levels. The output is
        printed in multiple columns if the size of the terminal supports it.
        """
        self._define_table_header()
        self._print_multicolumn()

    def _define_table_header(self):
        """Define table header."""
        hdict = {
            'levels': 'pressure levels',
            '2Dvars': '2D variables',
            '3Dvars': '3D variables'
        }
        self.header = "Available {}:".format(hdict[self.infotype])

    def _print_multicolumn(self):
        """Print a list of strings in several columns."""
        # get size of terminal window
        columns, rows = shutil.get_terminal_size(fallback=(80, 24))
        # maximum width of string in list
        maxwidth = max([len(x) for x in self.infolist])
        # calculate number of columns that fit on screen
        ncols = columns // (maxwidth + 2)
        # calculate number of rows
        nrows = - ((-len(self.infolist)) // ncols)
        # the number of columns may be reducible for that many rows.
        ncols = - ((-len(self.infolist)) // nrows)
        table = prettytable.PrettyTable([str(x) for x in range(ncols)])
        table.title = self.header
        table.header = False
        table.align = 'l'
        table.hrules = prettytable.NONE
        table.vrules = prettytable.NONE
        chunks = [self.infolist[i:i + nrows] for i in
                  range(0, len(self.infolist), nrows)]
        chunks[-1].extend('' for i in range(nrows - len(chunks[-1])))
        chunks = zip(*chunks)
        for c in chunks:
            table.add_row(c)
        print(table)
