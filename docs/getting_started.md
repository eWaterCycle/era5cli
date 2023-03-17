
## Installation

For installation, multiple options are available depending on your setup:

=== "Overview"

    | Source | Status |
    |-|-|
    | PyPI (pip) | [![](https://badge.fury.io/py/era5cli.svg)](https://pypi.org/project/era5cli/) |
    | conda-forge | [![](https://anaconda.org/conda-forge/era5cli/badges/version.svg)](https://anaconda.org/conda-forge/era5cli) |
    | Github | [![](https://img.shields.io/github/commits-since/eWaterCycle/era5cli/latest.svg)](https://github.com/eWaterCycle/era5cli)


=== "pip"

    To install era5cli from PyPI, use the following command:

    ```
    pip install era5cli
    ```

=== "conda"

    era5cli has been packaged for conda-forge. It can be installed from there with:

    ```
    conda install era5cli -c conda-forge
    ```


=== "development version"

    The development version is available via GitHub. To install directly from GitHub, the following command can be used:

    ```
    pip install -U  git+https://github.com/eWaterCycle/era5cli.git
    ```


## Copernicus CDS credentials

To be able to use era5cli, you need to be [**registered** at the Copernicus Climate Data Service (CDS)](https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome).

After activating your account, **login** on the CDS website, go to your **profile page** (top right on the website), and view your **API keys** at the bottom of the page.

To configure era5cli to use these keys, open up the environment you installed era5cli in, and do:

```sh
era5cli config --uid ID_NUMBER --key "KEY"
```

*Where ID_NUMBER is your user ID (e.g. 123456) and "KEY" is your API key, inside double quotes (e.g. "4s215sgs-2dfa-6h34-62h2-1615ad163414").*

After running this command your ID and key are validated and stored inside your home folder, under `.config/era5cli.txt.`

## Your first request

Now you should be able to make a request for data from the CDS. A request you could run can be, for example:

```sh
era5cli monthly --variables soil_type --startyear 2000 --months 01
```

Which will download the monthly mean `soil_type` data, for January 2000.

*Note: this file is ~2 MB*
