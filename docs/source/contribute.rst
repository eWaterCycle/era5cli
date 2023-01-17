Contribute
**********

Bug reports
===========

File bug reports or feature requests, and make contributions (e.g. code
patches), by `opening a new issue on GitHub <https://github.com/ewatercycle/era5cli/issues>`_.

Please give as much information as you can in the issue. It is very useful if
you can supply the command or a small self-contained code snippet that
reproduces the problem. Please also specify the era5cli version that you are
using and the version of the cdsapi library installed.

Contribute to the tool
======================

Create and activate the development environment:
::

    python3 -m venv env
    . env/bin/activate


Populate the development environment with the required dependencies:
::

    pip install -U pip
    pip install -e .[dev]

Before pushing a new addition, some tools are required to confirm that the code
is up to standard.

Use pytest to run the test suite:
::

   pytest

Use flake8 to check for code style issues:
::

   flake8 .

And lastly, format the code and sort the imports using black and isort:
::

   black .
   isort .

Deactivate the environment with:
::

   deactivate


Contribute to the documentation
===============================

When updating the documentation, use the environment created above.

Build the documentation with:
::

   sphinx-build docs/source docs/build
