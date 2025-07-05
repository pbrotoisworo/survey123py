YAML Construction Guide
=======================

This guide provides comprehensive instructions for building YAML files that Survey123Py can convert to Survey123-compatible Excel files.

Overview
--------

Survey123Py uses YAML files to define surveys in a human-readable format, which are then converted to Excel files with proper Survey123 formatting. Each YAML file contains three main sections:

- **settings**: Form configuration and metadata
- **choices**: Choice lists for select questions
- **survey**: The actual survey questions and structure

Understanding the "-" Syntax
-----------------------------

The YAML "-" (dash) syntax indicates a list item. In Survey123Py:

- Each "-" in the **survey** section represents a **single row** in the Excel survey sheet
- Each "-" in the **choices** section represents a **single row** in the Excel choices sheet
- The fields within each list item map to **specific Excel columns**

Example::

    survey:
      - type: text          # First row. "text" will be written to the cell in the "type" column in Excel
        name: q1            # "q1" will be written in the "name" column
        label: Your name?   # "Your name?" will be written in the "label" column
      - type: integer       # This creates a second row in Excel
        name: q2
        label: Your age?

Excel Column Mappings
---------------------

Survey Sheet Columns
~~~~~~~~~~~~~~~~~~~~

Each question (marked with "-") in the survey section maps to these Excel columns:

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - YAML Field
     - Excel Column
     - Description
   * - type
     - A
     - Question type (text, integer, select_one, etc.)
   * - name
     - B
     - Unique identifier for the question
   * - label
     - C
     - Display text shown to users
   * - hint
     - D
     - Additional help text
   * - guidance_hint
     - E
     - Extended guidance information
   * - appearance
     - F
     - Visual styling options
   * - required
     - G
     - Whether question is mandatory (yes/no)
   * - required_message
     - H
     - Custom message when required field is empty
   * - readonly
     - I
     - Whether field is read-only (yes/no)
   * - default
     - J
     - Default value for the field
   * - calculation
     - K
     - Formula for calculated fields
   * - constraint
     - L
     - Validation rules
   * - constraint_message
     - M
     - Message shown when constraint fails
   * - relevant
     - N
     - Logic for when question appears
   * - choice_filter
     - O
     - Filter choices dynamically
   * - repeat_count
     - P
     - Number of repetitions for repeat groups
   * - media::audio
     - Q
     - Audio file reference
   * - media::image
     - R
     - Image file reference
   * - bind::type
     - S
     - Data type binding
   * - bind::esri:fieldType
     - T
     - Esri field type
   * - bind::esri:fieldLength
     - U
     - Maximum field length
   * - bind::esri:fieldAlias
     - V
     - Display alias for field
   * - body::esri:style
     - W
     - Esri styling options
   * - bind::esri:parameters
     - X
     - Additional Esri parameters
   * - parameters
     - Y
     - General parameters
   * - body::accept
     - Z
     - Accepted file types
   * - body::esri:visible
     - AA
     - Visibility settings
   * - body::esri:inputMask
     - AB
     - Input formatting mask

Choices Sheet Columns
~~~~~~~~~~~~~~~~~~~~~

Each choice (marked with "-") in the choices section maps to these Excel columns:

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - YAML Field
     - Excel Column
     - Description
   * - list_name
     - A
     - Name of the choice list
   * - name
     - B
     - Internal value for the choice
   * - label
     - C
     - Display text for the choice
   * - media::audio
     - D
     - Audio file for the choice
   * - media::image
     - E
     - Image file for the choice

Settings Sheet Columns
~~~~~~~~~~~~~~~~~~~~~~

Settings fields map to these Excel columns:

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - YAML Field
     - Excel Column
     - Description
   * - form_title
     - A
     - Title of the form
   * - form_id
     - B
     - Unique form identifier
   * - instance_name
     - C
     - Instance naming pattern
   * - submission_url
     - D
     - URL for form submissions
   * - default_language
     - E
     - Default language code
   * - version
     - F
     - Form version number
   * - style
     - G
     - Form styling options
   * - namespaces
     - H
     - XML namespaces

YAML Structure Examples
-----------------------

Basic Survey Structure
~~~~~~~~~~~~~~~~~~~~~~

::

    settings:
      form_title: "My Survey"
      instance_name: "survey_${q1}"
    
    choices:
      - list_name: yes_no
        name: yes
        label: "Yes"
      - list_name: yes_no
        name: no
        label: "No"
    
    survey:
      - type: text
        name: q1
        label: "What is your name?"
        required: yes
      - type: select_one yes_no
        name: q2
        label: "Do you agree?"

Question Types
~~~~~~~~~~~~~~

**Text Questions**::

    - type: text
      name: name_field
      label: "Enter your name"
      required: yes
      hint: "First and last name"

**Integer Questions**::

    - type: integer
      name: age_field
      label: "Enter your age"
      constraint: ". > 0 and . < 120"
      constraint_message: "Age must be between 1 and 119"

**Select Questions**::

    - type: select_one colors
      name: favorite_color
      label: "What is your favorite color?"
      appearance: "minimal"

**Calculated Fields**::

    - type: text
      name: full_name
      label: "Full Name"
      calculation: "concat(${first_name}, ' ', ${last_name})"
      readonly: yes

**Note Fields**::

    - type: note
      name: instructions
      label: "Please answer all questions carefully"

Groups and Repeats
~~~~~~~~~~~~~~~~~~

**Groups** (questions grouped together)::

    - type: group
      name: personal_info
      label: "Personal Information"
      children:
        - type: text
          name: first_name
          label: "First Name"
        - type: text
          name: last_name
          label: "Last Name"

**Repeats** (repeating sections)::

    - type: repeat
      name: family_members
      label: "Family Members"
      children:
        - type: text
          name: member_name
          label: "Member Name"
        - type: integer
          name: member_age
          label: "Member Age"

Choice Lists
~~~~~~~~~~~~

**Simple Yes/No List**::

    choices:
      - list_name: yes_no
        name: yes
        label: "Yes"
      - list_name: yes_no
        name: no
        label: "No"

**Multiple Choice List**::

    choices:
      - list_name: colors
        name: red
        label: "Red"
      - list_name: colors
        name: blue
        label: "Blue"
      - list_name: colors
        name: green
        label: "Green"

**Choices with Images**::

    choices:
      - list_name: animals
        name: cat
        label: "Cat"
        media::image: "cat.jpg"
      - list_name: animals
        name: dog
        label: "Dog"
        media::image: "dog.jpg"

Advanced Features
-----------------

Variable Substitution
~~~~~~~~~~~~~~~~~~~~~

Use ``${variable_name}`` syntax to reference other fields::

    - type: text
      name: first_name
      label: "First Name"
    - type: note
      name: greeting
      label: "Hello ${first_name}!"

Conditional Logic
~~~~~~~~~~~~~~~~~

Use the ``relevant`` field to show/hide questions::

    - type: select_one yes_no
      name: has_children
      label: "Do you have children?"
    - type: integer
      name: num_children
      label: "How many children?"
      relevant: "${has_children} = 'yes'"

Validation Rules
~~~~~~~~~~~~~~~~

Use ``constraint`` for validation::

    - type: integer
      name: age
      label: "Age"
      constraint: ". >= 18"
      constraint_message: "You must be at least 18 years old"

Default Values
~~~~~~~~~~~~~~

Set default values for fields::

    - type: text
      name: country
      label: "Country"
      default: "USA"

Appearance Options
~~~~~~~~~~~~~~~~~~

Control how questions appear::

    - type: select_one colors
      name: color
      label: "Choose color"
      appearance: "minimal"    # dropdown instead of radio buttons

Media Integration
~~~~~~~~~~~~~~~~~

Add audio or image prompts::

    - type: text
      name: description
      label: "Describe what you see"
      media::image: "photo.jpg"
      media::audio: "instructions.mp3"

Testing and Preview
-------------------

Preview Input Fields
~~~~~~~~~~~~~~~~~~~~

Add test data using the ``survey123py::preview_input`` field::

    - type: text
      name: name
      label: "Your name"
      survey123py::preview_input: "John Doe"

This allows you to test variable substitution and preview your form with sample data.

Common Patterns
---------------

Required Fields
~~~~~~~~~~~~~~~

::

    - type: text
      name: email
      label: "Email Address"
      required: yes
      required_message: "Email is required"

Read-only Calculated Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    - type: text
      name: timestamp
      label: "Submission Time"
      calculation: "now()"
      readonly: yes

Conditional Sections
~~~~~~~~~~~~~~~~~~~~

::

    - type: select_one yes_no
      name: need_help
      label: "Do you need assistance?"
    - type: group
      name: help_section
      label: "Help Information"
      relevant: "${need_help} = 'yes'"
      children:
        - type: text
          name: help_type
          label: "What kind of help do you need?"

Best Practices
--------------

1. **Use descriptive names**: Field names should be clear and consistent
2. **Group related questions**: Use groups to organize related questions
3. **Add hints**: Provide helpful hints for complex questions
4. **Validate input**: Use constraints to ensure data quality
5. **Test thoroughly**: Use preview inputs to test your form logic
6. **Keep it simple**: Don't overcomplicate the structure

Common Errors to Avoid
----------------------

1. **Duplicate names**: Each field must have a unique name
2. **Invalid choice references**: Ensure choice lists exist before referencing them
3. **Circular references**: Don't create loops in variable substitutions
4. **Missing required fields**: Include all mandatory fields for your question types
5. **Incorrect boolean values**: Use "yes"/"no" strings, not true/false

Example Complete Survey
-----------------------

::

    settings:
      form_title: "Customer Feedback Survey"
      instance_name: "feedback_${customer_name}_${today()}"
      namespaces: "esri=https://esri.com/xforms"
    
    choices:
      - list_name: satisfaction
        name: very_satisfied
        label: "Very Satisfied"
      - list_name: satisfaction
        name: satisfied
        label: "Satisfied"
      - list_name: satisfaction
        name: neutral
        label: "Neutral"
      - list_name: satisfaction
        name: dissatisfied
        label: "Dissatisfied"
      - list_name: satisfaction
        name: very_dissatisfied
        label: "Very Dissatisfied"
      
      - list_name: yes_no
        name: yes
        label: "Yes"
      - list_name: yes_no
        name: no
        label: "No"
    
    survey:
      - type: text
        name: customer_name
        label: "Customer Name"
        required: yes
        survey123py::preview_input: "John Smith"
      
      - type: select_one satisfaction
        name: overall_satisfaction
        label: "How satisfied are you with our service?"
        required: yes
        
      - type: select_one yes_no
        name: would_recommend
        label: "Would you recommend us to others?"
        required: yes
        
      - type: text
        name: improvement_suggestions
        label: "What could we improve?"
        relevant: "${overall_satisfaction} = 'dissatisfied' or ${overall_satisfaction} = 'very_dissatisfied'"
        
      - type: group
        name: contact_info
        label: "Contact Information (Optional)"
        children:
          - type: text
            name: email
            label: "Email Address"
            hint: "We'll only use this for follow-up if needed"
          - type: text
            name: phone
            label: "Phone Number"
            
      - type: text
        name: submission_id
        label: "Submission ID"
        calculation: "concat('FB_', ${customer_name}, '_', format-date(today(), '%Y%m%d'))"
        readonly: yes

This creates a complete customer feedback survey with conditional logic, validation, and automatic ID generation.