Quick Start Guide
=================

This guide will help you get started with Survey123Py quickly.

Basic Usage
-----------

1. Create a YAML survey definition file
2. Use the command line tool to convert it to Excel
3. Import the Excel file into Survey123

Command Line Usage
------------------

Generate a Survey123 form from YAML:

.. code-block:: bash

   python main.py -v 3.22 --input sample_survey.yaml --output custom_output.xlsx

Available options:

* ``-v, --version``: Survey123 version (currently supports 3.22)
* ``--input``: Path to input YAML file
* ``--output``: Path for output Excel file

YAML Structure
--------------

Your YAML file should follow this basic structure:

.. code-block:: yaml

   survey:
     - type: text
       name: respondent_name
       label: "What is your name?"
       required: true
   
   choices: []
   
   settings:
     form_title: "My Survey"
     form_id: "my_survey"

Testing Your Survey
-------------------

Use the preview functionality to test your survey with sample data:

.. code-block:: python

   from survey123py.preview import FormPreviewer
   
   previewer = FormPreviewer()
   previewer.load_survey("your_survey.yaml")
   result = previewer.preview()

The preview system supports variable substitution using ``${variable}`` syntax and requires ``survey123py::preview_input`` fields in your YAML for test data.