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

- `.zenodo.json`
- `CITATION.cff`
- `era5cli/__version__.py`

## Confirm release info
Ensure the right date and upcoming version number (including release candidate
tag, if applicable) is set in:

- `CITATION.cff`
- `era5cli/__version__.py`

## Update the changelog
Update `CHANGELOG.rst` with new features and fixes in the upcoming version.
Confirm that `README.rst` is up to date with new features as well.

## Release on GitHub
Open [releases](https://github.com/eWaterCycle/era5cli/releases) and draft a new
release. Copy the changelog for this version into the description (though note
that the description is in Markdown, so reformat from Rst if necessary).

Tag the release according to [semantic versioning
guidelines](https://semver.org/), preceded with a `v` (e.g.: v1.0.0). The
release title is the tag and the release date together (e.g.: v1.0.0
(2019-07-25)).

### Release candidate
When releasing a release candidate on Github, tick the pre-release box, and
amend the version tag with `-rc` and the candidate number. Ensure the release
candidate version is accurate in `CITATION.cff` and `era5cli/__version__.py`.
If the version number in these files is not updated, Zenodo release
workflows will fail.

Releasing a release candidate is not required, but can help detect bugs early.

## PyPI release workflow
Publishing a new release in github triggers the github Action workflow that
builds and publishes the package to test.PyPI or PyPI. Versions with "rc"
(release candidate) in their version tag will only be published to test.PyPI.
Other version tags will trigger a PyPI release. Inspect
`.github/workflows/publish-to-pypi.yml` for more information.

Confirm a release candidate on test.PyPI with:
```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ era5cli
```

## Release on Zenodo
Confirm the new release on [Zenodo](https://doi.org/10.5281/zenodo.3252665).

## Release on the Research Software Directory
Wait a few hours, then confirm the addition of a new release on the
[RSD](https://www.research-software.nl/software/era5cli).
