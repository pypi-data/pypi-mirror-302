Install the package
-------------------

Directly from :pypi:`pyyc`::

  $ pip install pyyc

or by cloning the gitlab repository::

  $ git clone https://gitlab.in2p3.fr/ycopin/pyyc  # cloning
  $ cd pyyc
  [pyyc/]$ pip install .                           # local installation

Test the installation
---------------------

To test the package from Python (preferentially not from top-level directory):

>>> import pyyc
Initialization top-level module
Initialization sub-package A module A1
Initialization sub-package A module A2
Initialization sub-package B module + sub-package A module A1

To tests the main entries::

  $ python -m pyyc 1 abc
  [...]
  Command line arguments: ['1', 'abc']
  $ pyyc 2 def
  [...]
  Command line arguments: ['2', 'def']
  $ pyyc_addition 1 2
  [...]
  1 + 2 = 3

Build the documentation
-----------------------

To build the documentation from documentation directory::

  [docs/]$ make html
  [docs/]$ firefox _build/html/index.html
  [docs/]$ make latexpdf
  [docs/]$ evince _build/latex/pyyc.pdf

Run the tests
-------------

To run the doctests from source directory::

  [pyyc/]$ python -m doctest -v mod.py

or::

  [pyyc/]$ pytest --doctest-modules -v mod.py

To run the tests from top-level directory::

  $ pytest

To assess test coverage::

  $ coverage run -m pytest
  $ coverage report
  $ coverage html
  Wrote HTML report to htmlcov/index.html
  $ firefox htmlcov/index.html
