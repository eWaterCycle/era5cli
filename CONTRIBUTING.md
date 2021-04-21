# In general
Contributions are very welcome. Please make sure there is a github issue
associated with with every pull request. Creating an issue is also a good
way to propose new features.

# Readthedocs
For technical assistance with your contribution, please check the [contributing
guidelines on
readthedocs](https://era5cli.readthedocs.io/en/latest/contribute.html).

# Making a release

## Author information
Ensure all authors are present in:

- .zenodo.json
- CITATION.cff
- era5cli/__version__.py

## Confirm release info
Ensure the right date and upcoming version number is set in:

- CITATION.cff
- era5cli/__version__.py


## PyPI release workflow
Publishing a new release in github triggers the github Action workflow that
builds and publishes the package to test.PyPI and PyPI. Versions with "rc"
(releasecandidate) in their version tag will only be published to test.PyPI.
Other version tags will also trigger a PyPI release.
Inspect `.github/workflows/pyproject.toml` for more information.
