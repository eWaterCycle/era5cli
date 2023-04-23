# General development

## Installation

For a full development enviroment run the commands below.

!!! note
    This is optional: if you already have [`hatch`](https://hatch.pypa.io/) in your main environment, this setup is not needed, as you can use the `hatch` environments to run all commands.

=== "Unix"
    ```sh
    # Create a virtual environment, e.g. with
    python3 -m venv env_name

    # activate virtual environment
    source env_name/bin/activate

    # make sure to have a recent version of pip and hatch
    python3 -m pip install --upgrade pip hatch

    # (from the project root directory:)
    # install era5cli as an editable package, along with the dev dependencies
    python3 -m pip install --no-cache-dir --editable .[dev]
    ```

=== "Windows"
    ```sh
    # Create a virtual environment, e.g. with
    python -m venv env_name

    # activate virtual environment
    env_name/Scripts/Activate.ps1

    # make sure to have a recent version of pip and hatch
    python -m pip install --upgrade pip hatch

    # (from the project root directory:)
    # install era5cli as an editable package, along with the dev dependencies
    pip install --no-cache-dir --editable .[dev]
    ```

## Testing commands

As the project is set up with `hatch`, you can test changes made to the code by running, for example:

```sh
hatch run era5cli info 2Dvars
```

This will run the *local* era5cli code in a virtual environment.

## Running unit tests

era5cli uses `pytest` for unit testing. Running tests has been configured using `hatch`, and can be started by running:

```sh
hatch run test
```

In addition to just running the tests to see if they pass, they can be used for coverage statistics, i.e. to determine how much of the package’s code is actually executed during tests. Inside the package directory, run:

```sh
hatch run coverage
```

This runs tests and prints the results to the command line, as well as storing the result in a `coverage.xml` file (for analysis by, e.g. CodeCov or SonarCloud).

## Running formatters and linters
For linting and code style we use `flake8`, `black` and `isort`. All tools can simply be run by doing:

```sh
hatch run lint
```

To easily comply with `black` and `isort`, you can also run:

```sh
hatch run format
```

This will apply the `black` and `isort` formatting, and then check the code style.

## Generating the documentation

To view the documentation locally, simply run the following command:

```sh
hatch run docs:serve
```

The docs can also be built using `hatch run docs:build`.

## Versioning

Bumping the version across all files is done with bumpversion, e.g.

```sh
bumpversion major
bumpversion minor
bumpversion patch
```

## Making a release

This section describes how to make a release in 3 parts: preparation, release and validation.

### Preparation
1. Update the `docs/CHANGELOG.md` file.
2. Verify that the information in CITATION.cff is correct, and that the `era5cli/__version__.py` is up to date as well.
3. Make sure the version has been updated.
4. Run the unit tests with `hatch run test`.

### Making the GitHub release
Make a release and tag on GitHub.com.
Open [releases](https://github.com/eWaterCycle/era5cli/releases) and draft a new release.
Copy the changelog for this version into the description.
Tag the release according to [semantic versioning guidelines](https://semver.org/), preceded with a `v` (e.g.: v1.0.0).
The release title is the tag and the release date together (e.g.: v1.0.0 (2019-07-25)).

??? note "Release candidates"
    When releasing a release candidate on Github, tick the pre-release box, and amend the version tag with `-rc` and the candidate number.
    Ensure the release candidate version is accurate in `CITATION.cff` and `era5cli/__version__.py`.
    If the version number in these files is not updated, Zenodo release workflows will fail.

    Publishing a new release in github triggers the github Action workflow that builds and publishes the package to test.PyPI or PyPI.
    Versions with "rc" (release candidate) in their version tag will only be published to test.PyPI.
    Other version tags will trigger a PyPI release.
    Inspect `.github/workflows/publish-to-pypi.yml` for more information.

    Confirm a release candidate on test.PyPI with:
    ```
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ era5cli
    ```

The release will:

 - trigger Zenodo into making a snapshot of your repository and sticking a DOI on it.
 - start a GitHub action that builds and uploads the new version to [PyPI](https://pypi.org/project/era5cli/).
    - Which should trigger [conda-forge](https://github.com/conda-forge/era5cli-feedstock) to update the package as well.

### Validation
After making the release, you should check that:

1. The [Zenodo page](https://doi.org/10.5281/zenodo.3252665) is updated
2. The publishing action ran successfully, and that `pip install era5cli` installs the new version.
3. The [conda-forge package](https://anaconda.org/conda-forge/era5cli) is updated, and can be installed using conda.
4. Wait a few hours, then confirm the addition of a new release on the [RSD](https://www.research-software.nl/software/era5cli).

??? note "Adding contributors to the Research Software Directory (RSD)"
    If any contributors have been added, or the description of the software has changed, this can be edited (by eScience Center employees) via the [RSD admin interface](https://www.research-software.nl/admin/).
    More information about this process (e.g. how to add a new contributor or new affiliation) can be found in the [RSD documentation](https://github.com/research-software-directory/research-software-directory/blob/master/docs/entering-data.md) or in [this blogpost](https://blog.esciencecenter.nl/the-research-software-directory-and-how-it-promotes-software-citation-4bd2137a6b8).

??? note "Maintaining the conda-forge release"
    The new release on pypi will trigger the [conda-forge feedstock](https://github.com/conda-forge/era5cli-feedstock) to be automatically updated.

    If nothing changed to the built configuration, the automatic pull request should pass all tests, and can be merged by one of the maintainers.

    If the built changed, you can fork the feedstock repository to your own account, re-generate the `recipes/meta.yml` file (for example with [Grayskull](https://github.com/conda/grayskull)), and create a pull request to the feedstock.
