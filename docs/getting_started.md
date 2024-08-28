
## Installation

For installation, multiple options are available depending on your setup:

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

*****

| **Source** | PyPI (pip) | conda-forge | Github |
|------------|------------|-------------|--------|
| **Status** | [![](https://badge.fury.io/py/era5cli.svg)](https://pypi.org/project/era5cli/) | [![](https://anaconda.org/conda-forge/era5cli/badges/version.svg)](https://anaconda.org/conda-forge/era5cli) | [![](https://img.shields.io/github/commits-since/eWaterCycle/era5cli/latest.svg)](https://github.com/eWaterCycle/era5cli) |

## Copernicus CDS credentials

To be able to use era5cli, you need to be [**registered**](https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome) at the Copernicus Climate Data Service (CDS).

After activating your account, **login** on the CDS website, go to your **profile page** (top right on the website), and view your **API keys** at the bottom of the page.

To configure era5cli to use these keys, open up the environment you installed era5cli in, and do:

```sh
era5cli config --key "KEY"
```

*Where "KEY" is your API key, inside double quotes (e.g. "4s215sgs-2dfa-6h34-62h2-1615ad163414").*

After running this command your ID and key are validated and stored inside your home folder, under `.config/era5cli/cds_key.txt`.

!!! note
    If you already have a `.cdsapirc` file for the CDS api (or older version of era5cli), you will be asked if you want to copy these keys upon making an `era5cli` request.

## Your first request

Now you should be able to make a request for data from the CDS. For example:

```sh
era5cli monthly --variables soil_type --startyear 2000 --months 01
```

Which will download the monthly mean `soil_type` data, for January 2000.

*Note: this file is ~2 MB*
