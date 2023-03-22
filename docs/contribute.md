# Contributing to era5cli

## Bug reports

File bug reports or feature requests, and make contributions (e.g. code
patches), by [opening a new issue on GitHub](https://github.com/ewatercycle/era5cli/issues).

Please give as much information as you can in the issue. It is very useful if
you can supply the command or a small self-contained code snippet that
reproduces the problem. Please also specify the era5cli version that you are
using and the version of the cdsapi library installed.

## Contribute to the tool

Make sure `pip` and `hatch` are up to date:
```
python3 -m pip install pip hatch --upgrade
```

Create and activate the development environment:

```
hatch shell  # Or: python3 -m hatch shell
```

This will start a virtual environment with the required dependencies to allow for
development. Run this command before trying out any changes made to the code.

Before pushing a new addition, some checks are required to confirm that the code
is up to standard.

To run the test suite:
```
hatch run test
```

To format the code, and check the code styling:
```
hatch run format
```

Exit the the environment with:
```
exit
```

### Contribute to the documentation

When updating the documentation, build the documentation with:

```
hatch run docs:build
```
