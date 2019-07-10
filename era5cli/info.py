"""Print ERA5 information on available variables and levels."""

import era5cli.inputref as ref
from era5cli.utils import _print_multicolumn


class Info:
    """Print ERA5 information on available variables and levels.

    Parameters
    ----------
        infoname: str
            Name of information that needs to be printed. Supported are
            'levels', '2Dvars', '3Dvars' and any variable or pressure level
            defined in era5cli.inputref

    Raises
    ------
    AttributeError
        If `infoname` is not any of the supported strings.
    """

    def __init__(self, infoname: str):
        """Initialization of Info class."""
        self.infoname = infoname
        """str: Name of information that needs to be printed."""
        self.infotype = None
        """str: Type of information that needs to be printed."""
        self.infolist = []
        """list: List with information to be printed."""
        try:
            self.infolist = ref.REFDICT[self.infoname]
            """list: List with information to be printed."""
            self.infotype = "list"
        except KeyError:
            for valname, vallist in ref.REFDICT.items():
                if self.infoname in vallist:
                    self.infotype = valname
        if self.infotype is None:
            raise ValueError('Unknown value for reference argument.')

    def list(self):
        """Print a list of available variables or pressure levels.

        Prints a list of available variables or pressure levels. The output is
        printed in multiple columns if the size of the terminal supports it.
        """
        self._define_table_header()
        _print_multicolumn(self.header, self.infolist)

    def vars(self):
        """Return the  variable name or pressure level.

        Print in which list the given variable occurs.
        """
        print("{} is in the list: {}".format(self.infoname, self.infotype))

    def _define_table_header(self):
        """Define table header."""
        hdict = {
            'levels': 'pressure levels',
            '2Dvars': '2D variables',
            '3Dvars': '3D variables'
        }
        self.header = "Available {}:".format(hdict[self.infoname])
