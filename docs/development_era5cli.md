# era5cli specifics

## era5cli code structure

The typical flow of a CLI call through era5cli is as follows:

1. The call is parsed by the argparser in `cli.py`, leading to an `argparse.Namespace`
    - the specific subparsers and arguments are defined in `args/*.py`
2. If the command is `info` or `config`, those specific routines are called, and the program ends.
3. Otherwise, the "Fetch" is built and executed.
4. The Fetch object is defined in `fetch.py`, and:
    - asserts that the user has valid CDS login info
    - gathers the request parameters
    - splits up the request over variables, years (and optionally months).
    - sends the requests to a thread Pool
5. The requests are made to the CDS using the (Python) CDS API.

## Updating the variable reference
Occasionally changes are made to the ERA5 output.

An overview of the different ERA5 variables is available [here](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation#heading-Parameterlistings).
No changelog for name changes or additions/removals exists.

The reference file (`inputref.py`) contains the names of all available variables and pressure levels.
