pyYC documentation
##################

:Version: |version| of |today|
:Author: Yannick Copin <y.copin@ipnl.in2p3.fr>

:Abstract: This package should be used as a template for package
           structure, configuration and packaging, documentation,
           tests, gitlab continuous integration, etc. *Work In
           Progress, feedback is welcome!*

..
   PyPY does not support sphinx markup in top-level README. Keep it minimal,
   and add full description in documentation.

.. include:: ../README.rst

Quick introduction
==================

.. toctree::

   intro

Detailed documentation
======================

.. toctree::

   details

.. toctree::
   :hidden:

   __main__
   setup
   conf
   gitlab-ci

Code documentation
==================

.. toctree::
   :caption: Packages and modules

   pyyc

.. toctree::
   :titlesonly:
   :caption: Main entries

   main

.. toctree::
   :titlesonly:
   :caption: Tests

   tests

Notebooks
=========

.. toctree::
   :titlesonly:

   notebooks/pyyc.ipynb

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
