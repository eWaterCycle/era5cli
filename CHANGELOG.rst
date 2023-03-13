Release Notes
*************

Unreleased
~~~~~~~~~~
* Change CDS keys from .cdsapirc file to .config/eracli.txt file. This will avoid conflict with e.g. ADS.
* Add validator for era5cli.txt keys. This should provide better feedback to users and reduce user error.
* Added --splitmonths argument for `era5cli hourly`. This allows users to avoid a Request Too Large error.
* When a request would encounter a Request Too Large error in the CDS API, they are warned, and given a suggestion to use --splitmonths.
* If a user makes a request for hourly --land or --ensemble without --splitmonths they are warned that the behavior will change in the future.
* cli.py has been refactored to make the structure more clear. Seperate argument builders are now in their own modules.

1.3.2 (2021-12-13)
~~~~~~~~~~~~~~~~~~
* Elaborate the range of years that can be queried `#123 <https://github.com/eWaterCycle/era5cli/pull/123>`_
* Update Readthedocs theme `#125 <https://github.com/eWaterCycle/era5cli/pull/125>`_
* Fix a bug that allowed the incompatible combination of --land and --ensemble `#131 <https://github.com/eWaterCycle/era5cli/pull/131>`_

1.3.1 (2021-12-01)
~~~~~~~~~~~~~~~~~~
* Automatic Zenodo/RSD release failed; updated contribution guidelines `#106 <https://github.com/eWaterCycle/era5cli/pull/106>`_

1.3.0 (2021-11-30)
~~~~~~~~~~~~~~~~~~
* Fix compatibility with changed CDS variables geopotential/orography `#98 <https://github.com/eWaterCycle/era5cli/pull/98>`_
* Add integration testing `#102 <https://github.com/eWaterCycle/era5cli/pull/102>`_

1.2.1 (2021-04-21)
~~~~~~~~~~~~~~~~~~
* Automatic PyPI release for 1.2.0 failed; updated github action workflow `#91 <https://github.com/eWaterCycle/era5cli/pull/91>`_

1.2.0 (2021-04-21)
~~~~~~~~~~~~~~~~~~
* Add support for ERA5-Land data `#67 <https://github.com/eWaterCycle/era5cli/pull/67>`_
* Add functionality to download subregions `#70 <https://github.com/eWaterCycle/era5cli/pull/70>`_
* Update variables available for ERA5 datasets `#84 <https://github.com/eWaterCycle/era5cli/pull/84>`_

1.1.1 (2020-12-15)
~~~~~~~~~~~~~~~~~~
* Patch to fix the github actions publish automation `#64 <https://github.com/eWaterCycle/era5cli/pull/64>`_

1.1.0 (2020-12-14)
~~~~~~~~~~~~~~~~~~
* The stable 1.1.0 era5cli minor release.
* Add support for ERA5 preliminary back extension `#58 <https://github.com/eWaterCycle/era5cli/pull/58>`_
* Update tests `#57 <https://github.com/eWaterCycle/era5cli/pull/57>`_
* Add automated PyPI package building and publishing with github Actions `#62 <https://github.com/eWaterCycle/era5cli/pull/62>`_

1.0.0 (2019-07-25)
~~~~~~~~~~~~~~~~~~
* The stable 1.0.0 era5cli release.
* Adding more useful information to netCDF history `#48 <https://github.com/eWaterCycle/era5cli/pull/48>`_

1.0.0rc3 (2019-07-16)
~~~~~~~~~~~~~~~~~~~~~
* Third Release Candidate for the stable 1.0.0 era5cli release.
* Improve documentation `#21 <https://github.com/eWaterCycle/era5cli/issues/21>`_ `#29 <https://github.com/eWaterCycle/era5cli/issues/29>`_.
* Cleanup command line options `#19 <https://github.com/eWaterCycle/era5cli/issues/19>`_ `#20 <https://github.com/eWaterCycle/era5cli/issues/20>`_.
* Append era5cli version to history of downloaded netCDF file `#17 <https://github.com/eWaterCycle/era5cli/issues/17>`_.

1.0.0rc2 (2019-07-01)
~~~~~~~~~~~~~~~~~~~~~
* Second Release Candidate for the stable 1.0.0 era5cli release.
* Fix downloading all variables when requesting multiple variables and using --split `#23 <https://github.com/eWaterCycle/era5cli/issues/23>`_.
* Fix link to PyPI package in documentation `#22 <https://github.com/eWaterCycle/era5cli/issues/22>`_.

1.0.0rc1 (2019-06-22)
~~~~~~~~~~~~~~~~~~~~~
* First Release Candidate for the stable 1.0.0 era5cli release: A commandline utility to download ERA-5 data using cdsapi.
