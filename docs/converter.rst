Excel to YAML Converter
=======================

The Excel to YAML converter allows you to convert existing Survey123 Excel files back to YAML format. This is useful for:

* **Version control**: Store your surveys in a readable, version-controllable format
* **Migration**: Move from Excel-based to YAML-based survey development
* **Editing**: Make changes to existing surveys using the simplified YAML format
* **Backup**: Create human-readable backups of your survey definitions

Basic Usage
-----------

Command Line
~~~~~~~~~~~~

Convert an Excel file to YAML:

.. code-block:: bash

   python main.py convert --input survey.xlsx --output survey.yaml

With validation to ensure accuracy:

.. code-block:: bash

   python main.py convert --input survey.xlsx --output survey.yaml --validate

Python API
~~~~~~~~~~~

Use the converter programmatically:

.. code-block:: python

   from survey123py.converter import ExcelToYamlConverter
   
   # Create converter
   converter = ExcelToYamlConverter("3.22")
   
   # Convert Excel to YAML
   yaml_data = converter.convert_excel_to_yaml("survey.xlsx", "survey.yaml")
   
   # The yaml_data dictionary contains the converted data
   print(f"Converted {len(yaml_data['survey'])} questions")
   print(f"Found {len(yaml_data['choices'])} choice options")

Validation
----------

The converter includes validation functionality to ensure conversion accuracy:

.. code-block:: python

   from survey123py.converter import ExcelToYamlConverter
   
   converter = ExcelToYamlConverter("3.22")
   
   # Convert with validation
   yaml_data = converter.convert_excel_to_yaml("survey.xlsx", "survey.yaml")
   validation_results = converter.validate_conversion("survey.xlsx", "survey.yaml")
   
   if validation_results['success']:
       print("Conversion is accurate!")
   else:
       print("Validation warnings:")
       for warning in validation_results['warnings']:
           print(f"  - {warning}")

Features
--------

**Supported Elements**

* All question types (text, select_one, select_multiple, etc.)
* Choice lists and option definitions
* Form settings (title, instance name, etc.)
* Question properties (required, readonly, constraints, etc.)
* Groups and repeat sections
* Formulas and calculations

**Data Preservation**

* Question types and names
* Labels and hints
* Required and readonly flags
* Choice lists and options
* Form metadata and settings
* Nested structures (groups, repeats)

**Round-trip Compatibility**

The converter is designed for round-trip compatibility:

1. **Excel → YAML**: Convert existing Excel files to YAML
2. **YAML → Excel**: Use the standard generate command
3. **Validation**: Ensure data integrity throughout the process

Limitations
-----------

* Currently supports Survey123 version 3.22 only
* Some advanced Excel formatting may not be preserved
* Complex nested structures may require manual review
* Validation compares data structure, not visual formatting

Best Practices
--------------

**Before Converting**

1. **Backup**: Always backup your original Excel files
2. **Test**: Test the converted YAML by generating a new Excel file
3. **Validate**: Use the ``--validate`` option to check accuracy
4. **Review**: Manually review the converted YAML for complex surveys

**After Converting**

1. **Version Control**: Add the YAML files to your version control system
2. **Documentation**: Add comments to the YAML for future reference
3. **Testing**: Test the converted survey in Survey123 Connect
4. **Workflow**: Establish a YAML-first workflow for future changes

.. code-block:: bash

   # Recommended workflow
   python main.py convert --input original.xlsx --output survey.yaml --validate
   # Edit survey.yaml as needed
   python main.py generate --input survey.yaml --output updated.xlsx
   # Import updated.xlsx into Survey123 Connect

Troubleshooting
---------------

**Common Issues**

* **Missing data**: Check that all required sheets (survey, choices, settings) are present
* **Type errors**: Ensure question types are properly formatted
* **Validation failures**: Review differences and determine if they're acceptable
* **Encoding issues**: Ensure Excel files use UTF-8 encoding

**Getting Help**

If you encounter issues:

1. Check the validation results for specific problems
2. Review the generated YAML for obvious errors
3. Test with a simple Excel file first
4. Consult the API documentation for advanced usage