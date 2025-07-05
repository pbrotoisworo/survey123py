Survey123Py Documentation
=========================

Survey123Py is a Python library that converts YAML survey definitions into Survey123-compatible Excel files. It simplifies form creation by replacing Excel's 40+ column workflow with readable YAML configuration files.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   yaml-guide
   publishing
   api

Features
--------

* Convert YAML survey definitions to Survey123-compatible Excel files
* Simplified form creation workflow
* Support for Survey123 version 3.22
* Formula support with comprehensive operators
* Preview functionality for testing surveys

Installation
------------

Install Survey123Py directly from GitHub:

.. code-block:: bash

   pip install git+https://github.com/pbrotoisworo/survey123py.git

Quick Start
-----------

Create a YAML file with your survey definition and convert it to Excel:

.. code-block:: bash

   python main.py -v 3.22 --input sample_survey.yaml --output custom_output.xlsx

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`