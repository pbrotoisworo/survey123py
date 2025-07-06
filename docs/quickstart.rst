Quick Start Guide
=================

This guide will help you get started with Survey123Py quickly.

Basic Usage
-----------

**YAML to Excel Workflow (Recommended)**

1. Create a YAML survey definition file
2. Use the command line tool to convert it to Excel
3. Import the Excel file into Survey123

**Excel to YAML Workflow (Migration)**

1. Export your existing survey from Survey123 Connect as Excel
2. Use the converter to transform it to YAML
3. Edit the YAML file as needed
4. Generate a new Excel file for Survey123

Command Line Usage
------------------

Generate Command
~~~~~~~~~~~~~~~~

Generate a Survey123 form from YAML:

.. code-block:: bash

   python main.py generate -v 3.22 --input sample_survey.yaml --output custom_output.xlsx

Convert Command
~~~~~~~~~~~~~~~

Convert an existing Excel file back to YAML:

.. code-block:: bash

   python main.py convert --input existing_survey.xlsx --output converted_survey.yaml

Add validation to ensure round-trip accuracy:

.. code-block:: bash

   python main.py convert --input existing_survey.xlsx --output converted_survey.yaml --validate

Available options:

* ``-v, --version``: Survey123 version (currently supports 3.22)
* ``--input``: Path to input file (YAML for generate, Excel for convert)
* ``--output``: Path for output file (Excel for generate, YAML for convert)
* ``--validate``: Validate conversion accuracy (convert command only)

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