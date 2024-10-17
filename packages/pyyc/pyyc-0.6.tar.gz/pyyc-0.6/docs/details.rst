Packaging (`setup.cfg`)
-----------------------

The :ref:`setup.cfg` allows for easy packaging and installation::

  $ pip install pyyc

or through the complete cloning of the gitlab repository::

  $ git clone https://gitlab.in2p3.fr/ycopin/pyyc  # cloning
  $ cd pyyc
  $ pip install .                                  # local installation

Package initialization (`__init__.py`)
--------------------------------------

The `__init__.py` file in each package directory describes the
initialization of the package, i.e. the actions (usually imports, but
also definitions, etc.) to be performed at package import.

.. code-block:: python

   >>> import pyyc  # Will run pyyc/__init__.py and all subsequent initializations
   Initialization top-level module
   Initialization sub-package A module A1
   Initialization sub-package A module A2
   Initialization sub-package B module + sub-package A module A1
   >>> pyyc.subpkgA.modA1.version
   'sub-package A module A1'
   >>> pyyc.subpkgB.version
   'sub-package B module + sub-package A module A1'

Main entries (`__main__.py`)
----------------------------

The *main* program can be called in different ways:

* as the :ref:`__main__.py <main.py>` entry of a module, e.g.::

    $ python -m pyyc arg1 arg2     # Execute top-level pyyc/__main__.py
    Initialization top-level module
    Initialization sub-package A module A1
    Initialization sub-package A module A2
    Initialization sub-package B module + sub-package A module A1
    ---------------------- MAIN ----------------------
    Command line arguments: ['arg1', 'arg2']

  There can be only *one* package main, corresponding to the `if
  __name == "__main__"` part of the `__main__.py` file.

* as console scripts defined as *entry points* in :ref:`setup.cfg`:

  .. literalinclude:: ../setup.cfg
     :language: cfg
     :start-at: [options.entry_points]
     :end-before: [options.extras_require]

  These entry points are converted to plain scripts at installation::

    $ pyyc arg1 arg2               # Execute pyyc/__main__.py:main()
    Initialization top-level module
    Initialization sub-package A module A1
    Initialization sub-package A module A2
    Initialization sub-package B module + sub-package A module A1
    ---------------------- MAIN ----------------------
    Command line arguments: ['arg1', 'arg2']

    $ pyyc_addition 1 2            # Execute pyyc/__main__.py:main_addition()
    Initialization top-level module
    Initialization sub-package A module A1
    Initialization sub-package A module A2
    Initialization sub-package B module + sub-package A module A1
    1 + 2 = 3

Reference: https://setuptools.pypa.io/en/latest/userguide/entry_point.html

Documentation
-------------

The sample code is documented using the documentation generator
:pypi:`sphinx` within the dedicated directory `docs/`, typically for a
first use::

  [docs/]$ sphinx-quickstart  # initiate the documentation tool
  [docs/]$ # edit 'conf.py' to your needs (see below)
  [docs/]$ sphinx-apidoc -o . ../pyyc  # automatic generation of documentation files
  Creating file ./pyyc.rst.
  Creating file ./pyyc.subpkgA.rst.
  Creating file ./pyyc.subpkgB.rst.
  Creating file ./modules.rst.
  [docs/]$ # include these documentation files in 'index.rst' (see below)
  [docs/]$ make html          # build the documentation as a website
  [docs/]$ firefox _build/html/index.html

As an illustration, the online version of this documentation, using the
configuration file :ref:`conf.py`, is available at
https://ycopin.pages.in2p3.fr/pyyc/.  The automatically generated code
documentation part is under :ref:`index:Code documentation`.

`conf.py`
.........

In particular, the use of the auto-documentation extension
`sphinx.ext.autodoc` requires few non-trivial lines in :ref:`conf.py`:

* set-up the path to code sources for extraction of docstrings:

  .. literalinclude:: conf.py
     :language: python
     :start-at: import os, sys
     :end-at: sys.path.insert

* add `sphinx.ext.autodoc` in the list of sphinx extensions `extensions =
  [...]` (or initially add option `--ext-autodoc` to `sphinx-quickstart`)
* configure the `autodoc` extension:

  .. literalinclude:: conf.py
     :language: python
     :start-at: Autodoc configuration
     :end-at: autodoc_member_order

`index.rst`
...........

The `index.rst` file is the top-level documentation file, which will
include links to all the other documentation `.rst` files under the
specific `.. toctree::` command, e.g.:

.. code-block:: rest

   .. toctree::
      :caption: Code documentation
      :titlesonly:

      pyyc
      pyyc.subpkgA
      pyyc.subpkgB
      modules

`setup.cfg`
...........

.. WARNING:: setuptools integration (`build_sphinx`) is deprecated
   since Sphinx 5+, and removed from Sphinx 7+.  Alternative is to
   build doc manually (e.g. `make html`).

Notebooks
.........

If any, you can add notebooks directly to your documentation with the
:pypi:`nbsphinx` extension (which needs to be installed).

* add `nbsphinx` in the list of sphinx extensions `extensions =
  [...]`
* add notebooks stored in `docc/notebooks/` directory in a dedicated
  documentation section, e.g.:

   .. code-block:: rest

      Notebooks
      =========

      .. toctree::
         :titlesonly:

         notebooks/pyyc.ipynb

Testing
-------

.. Warning:: With the current configuration :ref:`setup.cfg` (considered
   deprecated for tests), it is not possible to run the tests directly from
   `setup.py`. It is therefore necessary to run the tests manually.

Doctests
........

Doctests (i.e. small examples and tests directly included in the docstrings)
can be performed on documented source code with either standard package
:mod:`doctest` or with external package :pypi:`pytest`::

  [pyyc/]$ python -m doctest -v mod.py
  [pyyc/]$ pytest --doctest-modules -v mod.py

Dedicated tests
...............

Tests gathered in the `tests/` directory shall be performed using
:pypi:`pytest`, e.g.::

  [tests/]$ pytest -v test_mod.py

`pytest` will actually auto-discover all the tests from top-level directory::

  $ pytest

Test coverage
.............

:pypi:`coverage` will run the test suite and look for parts of the code which
have been (and more importantly *not been*) tested.

::

  $ coverage run -m pytest
  $ coverage report
  Name                       Stmts   Miss  Cover
  ----------------------------------------------
  pyyc/__init__.py               4      0   100%
  pyyc/mod.py                   41      2    95%
  pyyc/subpkgA/__init__.py       3      0   100%
  pyyc/subpkgA/modA1.py          2      0   100%
  pyyc/subpkgA/modA2.py          2      0   100%
  pyyc/subpkgB/__init__.py       1      0   100%
  pyyc/subpkgB/modB.py           3      0   100%
  tests/__init__.py              0      0   100%
  tests/test_mod.py             40      0   100%
  ----------------------------------------------
  TOTAL                         96      2    98%

To visualize which parts of the code is documented or not::

  $ coverage html
  Wrote HTML report to htmlcov/index.html
  $ firefox htmlcov/index.html

Data files (e.g. `config/`)
---------------------------

Example to access data file at run-time:

.. code-block:: python

   >>> from pyyc.mod import read_config
   >>> cfg = read_config()  # will look for config file distributed with pyyc package
   Reading configuration from .../pyYC/pyyc/config/default.cfg...
   >>> cfg['DEFAULT']['version']
   'cfg-1.0'

This is controlled by section `[options.package_data]` in
:ref:`setup.cfg`:

.. literalinclude:: ../setup.cfg
   :language: cfg
   :start-at: [options.package_data]
   :end-before: [tool:pytest]

Reference: https://setuptools.pypa.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime

Gitlab continuous integration
-----------------------------

If the code is hosted in a GitLab repository, one can use `Continuous
methods <https://docs.gitlab.com/ee/ci/index.html>`_ with a dedicated
configuration file :ref:`.gitlab-ci.yml <gitlab-ci>` in the top-level
directory.  The current configuration will build and deploy the
documentation as a static website hosted on `GitLab pages
<https://docs.gitlab.com/ee/user/project/pages/>`_, namely
https://ycopin.pages.in2p3.fr/pyyc/ for `pyyc`.

More elements
-------------

For French-speaking users, you can have a look at the online course `Analyse
scientifique avec Python
<https://ycopin.pages.in2p3.fr/Informatique-Python/index.html>`_, and in
particular to the `packaging
<https://ycopin.pages.in2p3.fr/Informatique-Python/Cours/packaging.html>`_ section.


To do
-----

* Display directory structure and content based on `this recipe
  <https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python>`_
* Use `src/` as package directory name
* Use :pypi:`sphinx-test-reports`
* Use https://github.com/pypa/setuptools_scm
