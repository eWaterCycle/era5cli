# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

# 2.0.1 - 2025-04-04

Changes since v2.0.0:

**Changed:**
- Threads are set to 1 by default, as the new CDS is not faster if you use multiple threads.
  
**Fixed:**
- The cdsapi changed how wants the request formatted for getting netCDF files, netCDF files weren't properly downloaded anymore.

# 2.0.0 - 2025-02-12

Changes since v1.4.2:

**Added:**

 - support for Python 3.12, 3.13.

**Changed:**

 - The `splitmonths` argument now defaults to `True` for hourly requests. To not split requests by year, add `--splitmonths False`.
 - The 'cads-api-client' used in the 2.0 beta versions is already deprecated, the backend now uses the 'cdsapi' again, which uses ["datapi"](https://github.com/ecmwf-projects/datapi).

**Fixed:**

 - Added support for the new climate data store.

**Removed:**

 - the deprecated `orography` variable. Use `geopotential` instead.
 - the deprecated `--prelimbe` argument. This one has not been required anymore, as the back-extension is part of the normal dataset now.
 - support for Python 3.8.

**Dev changes:**

 - The pre-commit hook has been removed. Pre-commit does not play well with hatch: it would need to be installed system-wide. No hatch-specific hooks are available.



## 2.0.0b2 - 2024-09-20

**Fixed:**
 - Pinned the version number of `cads-api-client` as its interface is unstable.


## 2.0.0b1 - 2024-08-30

**Changed:**

 - The `splitmonths` argument now defaults to `True` for hourly requests. To not split requests by year, add `--splitmonths False`.

**Fixed:**

 - Added support for the beta-CDS
 - For authentication, the new `cads-api-client` is used, instead of a dummy request. This should avoid the dummy requests appearing in the user's queue.

**Removed:**

 - the deprecated `orography` variable. Use `geopotential` instead.
 - the deprecated `--prelimbe` argument. This one has not been required anymore, as the back-extension is part of the normal dataset now.

**Dev changes:**

 - The pre-commit hook has been removed. Pre-commit does not play well with hatch: it would need to be installed system-wide. No hatch-specific hooks are available.


## 1.4.2 - 2023-12-12

**Fixed:**

 - Fixed a typo in the error message when an invalid area was given ([#160](https://github.com/eWaterCycle/era5cli/pull/160)).
 - Fixed pressing Enter not working for the default input in the "*Valid CDS keys found in the .cdsapirc file. Do you want to use these for era5cli? [Y/n]*" prompt ([#160](https://github.com/eWaterCycle/era5cli/pull/160)).

**Added:**
 
 - era5cli is now available for Python 3.11 ([#160](https://github.com/eWaterCycle/era5cli/pull/160)).

**Removed:**

- Support for Python 3.7 has been removed. It's [end-of-life](https://devguide.python.org/versions/#unsupported-versions) was 2023-06-27 ([#160](https://github.com/eWaterCycle/era5cli/pull/160)).


## 1.4.1 - 2023-06-30
**Fixed:**

 - Fix a bug that prevented the creation of the configuration file, if the "~/.config" folder did not exist yet ([#154](https://github.com/eWaterCycle/era5cli/pull/154)).

**Added:**

- The developer documentation now contains instructions on how to maintain the conda-forge feedstock for era5cli ([#150](https://github.com/eWaterCycle/era5cli/pull/154)).

**Changed:**
 
 - Before asking for a user input, a check is made if the code is running in an interactive terminal or not. If not (e.g. if era5cli is called through a different script and stdin is not available), the input request is skipped ([#152](https://github.com/eWaterCycle/era5cli/pull/154)).

**Dev changes:**

 - A pre-commit hook has been added, to facilitate pre-commit users. Documentation on the setup is added to the developer documentation ([#153](https://github.com/eWaterCycle/era5cli/pull/154)). 


## 1.4.0 - 2023-04-21
**Added:**

 - Add validator for user's CDS keys. This should provide better feedback to users and reduce user error ([#138](https://github.com/eWaterCycle/era5cli/pull/138)).
 - Added `--splitmonths` argument for `era5cli hourly`. This allows users to avoid a Request Too Large error ([#139](https://github.com/eWaterCycle/era5cli/pull/139)).
 - When a request would encounter a Request Too Large error in the CDS API, they are warned, and given a suggestion to use the new `--splitmonths` argument ([#139](https://github.com/eWaterCycle/era5cli/pull/139)).
 - Added -`-dashed-varname` argument, to produce file names where the variable name is separated using dashes. For example: `soil-type` vs. `soil_type`. For the ongoing discussion, see [#53](https://github.com/eWaterCycle/era5cli/issues/53).

**Changed:**

 - Change CDS keys from cdsapi default `.cdsapirc` file to `.config/era5cli/cds_key.txt` file ([#138](https://github.com/eWaterCycle/era5cli/pull/138)).
   - This will avoid conflict with e.g. ADS keys
   - The user can configure the keys using `era5cli config`, no need to create a file in the right location.
 - When a request would encounter a Request Too Large error in the CDS API, they are warned, and given a suggestion to use `--splitmonths` ([#139](https://github.com/eWaterCycle/era5cli/pull/139)).
 - If a user makes a request without `--splitmonths` they are warned that the behavior will change in the future, and that they have to choose between `--splitmonths False` and `--splitmonths True`
 - When a file already exists and would be overwritten, the user is prompted for confirmation. This should prevent accidental overwriting of files. This check can be skipped with the `--overwrite` flag ([#143](https://github.com/eWaterCycle/era5cli/pull/143)).
 - The earliest valid start year of ERA5 requests has been updated to 1940 (for ERA5-land it is still 1950) ([#146](https://github.com/eWaterCycle/era5cli/pull/146)).
 - Usage of `--prelimbe` now raises a deprecation warning. It will be deprecated in a future release, as all the back extension years are now included in the main products ([#147](https://github.com/eWaterCycle/era5cli/pull/147)).
 - The documentation has been fully overhauled, and now uses Markdown files & MkDocs ([#142](https://github.com/eWaterCycle/era5cli/pull/142), [#144](https://github.com/eWaterCycle/era5cli/pull/144)).

**Dev changes:**

 - `cli.py` has been refactored to make the structure more clear. Seperate argument builders are now in their own modules ([#139](https://github.com/eWaterCycle/era5cli/pull/139)).

## 1.3.2 - 2022-12-13
**Changed:**

 - Elaborate the range of years that can be queried [#123](https://github.com/eWaterCycle/era5cli/pull/123)
 - Update Readthedocs theme [#125](https://github.com/eWaterCycle/era5cli/pull/125)

**Fixed:**

 - Fix a bug that allowed the incompatible combination of --land and --ensemble [#131](https://github.com/eWaterCycle/era5cli/pull/131)


## 1.3.1 - 2021-12-01
**Fixed:**

 - Automatic Zenodo/RSD release failed; updated contribution guidelines [#106](https://github.com/eWaterCycle/era5cli/pull/106)

## 1.3.0 - 2021-11-30
**Added:**

 - Add integration testing [#102](https://github.com/eWaterCycle/era5cli/pull/102)

**Fixed:**

 - Fix compatibility with changed CDS variables geopotential/orography [#98](https://github.com/eWaterCycle/era5cli/pull/98)

## 1.2.1 - 2021-04-21
**Fixed:**

 - Automatic PyPI release for 1.2.0 failed; updated github action workflow [#91](https://github.com/eWaterCycle/era5cli/pull/91)

## 1.2.0 - 2021-04-21
**Added:**

 - Add support for ERA5-Land data [#67](https://github.com/eWaterCycle/era5cli/pull/67)
 - Add functionality to download subregions [#70](https://github.com/eWaterCycle/era5cli/pull/70)

**Changed:**

 - Update variables available for ERA5 datasets [#84](https://github.com/eWaterCycle/era5cli/pull/84)

## 1.1.1 - 2020-12-15
**Fixed:**

 - Patch to fix the github actions publish automation [#64](https://github.com/eWaterCycle/era5cli/pull/64)

## 1.1.0 - 2020-12-14
The stable 1.1.0 era5cli minor release.

**Added:**

 - Add support for ERA5 preliminary back extension [#58](https://github.com/eWaterCycle/era5cli/pull/58)
 - Add automated PyPI package building and publishing with github Actions [#62](https://github.com/eWaterCycle/era5cli/pull/62)

**Changed:**

 - Update tests [#57](https://github.com/eWaterCycle/era5cli/pull/57)

## 1.0.0 - 2019-07-25
The stable 1.0.0 era5cli release.

**Added:**

 - Adding more useful information to netCDF history [#48](https://github.com/eWaterCycle/era5cli/pull/48)

## 1.0.0rc3 - 2019-07-16
Third Release Candidate for the stable 1.0.0 era5cli release.

**Added:**

 - Append era5cli version to history of downloaded netCDF file [#17](https://github.com/eWaterCycle/era5cli/issues/17)

**Changed:**

 - Improve documentation [#21](https://github.com/eWaterCycle/era5cli/issues/21) [#29](https://github.com/eWaterCycle/era5cli/issues/29)
 - Cleanup command line options [#19](https://github.com/eWaterCycle/era5cli/issues/19) [#20](https://github.com/eWaterCycle/era5cli/issues/20)

## 1.0.0rc2 - 2019-07-01
Second Release Candidate for the stable 1.0.0 era5cli release.

**Fixed:**

 - Fix downloading all variables when requesting multiple variables and using --split [#23](https://github.com/eWaterCycle/era5cli/issues/23)
 - Fix link to PyPI package in documentation [#22](https://github.com/eWaterCycle/era5cli/issues/22)

## 1.0.0rc1 - 2019-06-22
First Release Candidate for the stable 1.0.0 era5cli release: A commandline utility to download ERA-5 data using cdsapi.
