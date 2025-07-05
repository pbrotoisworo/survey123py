Testing and Previewing
======================

Survey123Py includes a powerful ``FormPreviewer`` class that allows you to test your survey forms with sample data before publishing. This is especially useful for validating formulas, calculations, and logic flows without needing to deploy to Survey123.

Overview
--------

The ``FormPreviewer`` uses a special field called ``survey123py::preview_input`` to provide test data for each question. When you run a preview, it simulates filling out the survey with your test data and shows you the results of all calculations, constraints, and formulas.

Basic Usage
-----------

Simple Preview Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # basic_preview.yaml
    settings:
      form_title: "Basic Preview Example"
    
    survey:
      - type: text
        name: first_name
        label: "What's your first name?"
        survey123py::preview_input: "John"
      
      - type: text
        name: last_name
        label: "What's your last name?"
        survey123py::preview_input: "Doe"
      
      - type: note
        name: full_name_display
        label: "Full name: ${first_name} ${last_name}"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    # Create previewer
    previewer = FormPreviewer("basic_preview.yaml")
    
    # Generate preview
    results = previewer.show_preview()
    
    # Check results
    print(results["survey"][2]["label"])  # Output: "Full name: John Doe"

Advanced Preview Examples
-------------------------

Testing Calculations
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # calculations_example.yaml
    settings:
      form_title: "Calculation Testing"
    
    survey:
      - type: decimal
        name: length
        label: "Length (meters)"
        survey123py::preview_input: 10.5
      
      - type: decimal
        name: width
        label: "Width (meters)"
        survey123py::preview_input: 8.2
      
      - type: calculate
        name: area
        calculation: "${length} * ${width}"
      
      - type: note
        name: area_display
        label: "Area: ${area} square meters"
      
      - type: calculate
        name: area_rounded
        calculation: "round(${area}, 2)"
      
      - type: note
        name: area_rounded_display
        label: "Rounded area: ${area_rounded} sq m"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    previewer = FormPreviewer("calculations_example.yaml")
    results = previewer.show_preview()
    
    # Check calculated values
    area = results["survey"][2]["calculation"]
    print(f"Calculated area: {area}")  # Output: 86.1
    
    area_display = results["survey"][3]["label"]
    print(area_display)  # Output: "Area: 86.1 square meters"
    
    rounded_area = results["survey"][4]["calculation"]
    print(f"Rounded area: {rounded_area}")  # Output: 86.1

Testing Formulas
~~~~~~~~~~~~~~~

.. code-block:: yaml

    # formulas_example.yaml
    settings:
      form_title: "Formula Testing"
    
    survey:
      - type: text
        name: email
        label: "Email address"
        survey123py::preview_input: "user@example.com"
      
      - type: calculate
        name: email_valid
        calculation: "regex('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', ${email})"
      
      - type: note
        name: email_status
        label: "Email valid: ${email_valid}"
      
      - type: text
        name: phone
        label: "Phone number"
        survey123py::preview_input: "123-456-7890"
      
      - type: calculate
        name: phone_formatted
        calculation: "regex('[0-9]{3}-[0-9]{3}-[0-9]{4}', ${phone})"
      
      - type: note
        name: phone_status
        label: "Phone format valid: ${phone_formatted}"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    previewer = FormPreviewer("formulas_example.yaml")
    results = previewer.show_preview()
    
    # Check formula results
    email_valid = results["survey"][1]["calculation"]
    phone_valid = results["survey"][4]["calculation"]
    
    print(f"Email validation: {email_valid}")  # Output: True
    print(f"Phone validation: {phone_valid}")  # Output: True

Testing Choice Logic
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # choice_logic_example.yaml
    settings:
      form_title: "Choice Logic Testing"
    
    choices:
      - list_name: yes_no
        name: yes
        label: "Yes"
      - list_name: yes_no
        name: no
        label: "No"
      
      - list_name: colors
        name: red
        label: "Red"
      - list_name: colors
        name: blue
        label: "Blue"
      - list_name: colors
        name: green
        label: "Green"
    
    survey:
      - type: select_one yes_no
        name: likes_colors
        label: "Do you like colors?"
        survey123py::preview_input: "yes"
      
      - type: select_multiple colors
        name: favorite_colors
        label: "Select your favorite colors"
        relevant: "${likes_colors} = 'yes'"
        survey123py::preview_input: "red green"
      
      - type: calculate
        name: color_count
        calculation: "count-selected(${favorite_colors})"
      
      - type: note
        name: color_summary
        label: "You selected ${color_count} colors"
        relevant: "${likes_colors} = 'yes'"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    previewer = FormPreviewer("choice_logic_example.yaml")
    results = previewer.show_preview()
    
    # Check choice logic
    color_count = results["survey"][2]["calculation"]
    summary_text = results["survey"][3]["label"]
    
    print(f"Colors selected: {color_count}")  # Output: 2
    print(summary_text)  # Output: "You selected 2 colors"

Testing Constraints
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # constraints_example.yaml
    settings:
      form_title: "Constraint Testing"
    
    survey:
      - type: integer
        name: age
        label: "Your age"
        constraint: ". >= 18 and . <= 120"
        constraint_message: "Age must be between 18 and 120"
        survey123py::preview_input: 25
      
      - type: text
        name: username
        label: "Username"
        constraint: "string_length(.) >= 3 and string_length(.) <= 20"
        constraint_message: "Username must be 3-20 characters"
        survey123py::preview_input: "john_doe"
      
      - type: decimal
        name: score
        label: "Test score (0-100)"
        constraint: ". >= 0 and . <= 100"
        constraint_message: "Score must be between 0 and 100"
        survey123py::preview_input: 87.5

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    previewer = FormPreviewer("constraints_example.yaml")
    results = previewer.show_preview()
    
    # Check constraint results
    for i, question in enumerate(results["survey"]):
        if "constraint_result" in question:
            constraint_passed = question["constraint_result"]
            name = question["name"]
            print(f"{name} constraint: {'PASS' if constraint_passed else 'FAIL'}")

Testing Date and Time Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # datetime_example.yaml
    settings:
      form_title: "Date and Time Testing"
    
    survey:
      - type: date
        name: birth_date
        label: "Birth date"
        survey123py::preview_input: "1990-05-15"
      
      - type: calculate
        name: birth_timestamp
        calculation: "date(${birth_date})"
      
      - type: calculate
        name: current_time
        calculation: "now()"
      
      - type: calculate
        name: age_days
        calculation: "(${current_time} - ${birth_timestamp}) div (1000 * 60 * 60 * 24)"
      
      - type: calculate
        name: age_years
        calculation: "round(${age_days} div 365.25, 1)"
      
      - type: note
        name: age_display
        label: "Approximate age: ${age_years} years"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    from datetime import datetime
    
    previewer = FormPreviewer("datetime_example.yaml")
    results = previewer.show_preview()
    
    # Check date calculations
    birth_timestamp = results["survey"][1]["calculation"]
    current_time = results["survey"][2]["calculation"]
    age_years = results["survey"][4]["calculation"]
    
    print(f"Birth timestamp: {birth_timestamp}")
    print(f"Current time: {current_time}")
    print(f"Calculated age: {age_years} years")

Complex Logic Testing
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # complex_logic_example.yaml
    settings:
      form_title: "Complex Logic Testing"
    
    choices:
      - list_name: employment_status
        name: employed
        label: "Employed"
      - list_name: employment_status
        name: unemployed
        label: "Unemployed"
      - list_name: employment_status
        name: student
        label: "Student"
      - list_name: employment_status
        name: retired
        label: "Retired"
    
    survey:
      - type: integer
        name: age
        label: "Your age"
        survey123py::preview_input: 28
      
      - type: select_one employment_status
        name: employment
        label: "Employment status"
        survey123py::preview_input: "employed"
      
      - type: integer
        name: income
        label: "Annual income (if employed)"
        relevant: "${employment} = 'employed'"
        survey123py::preview_input: 65000
      
      - type: calculate
        name: income_category
        calculation: "if(${income} < 30000, 'Low', if(${income} < 60000, 'Medium', 'High'))"
      
      - type: calculate
        name: eligibility_score
        calculation: "if(${age} >= 18 and ${employment} = 'employed' and ${income} >= 25000, 100, if(${age} >= 18 and ${employment} = 'student', 75, 25))"
      
      - type: note
        name: results_summary
        label: "Income category: ${income_category}, Eligibility score: ${eligibility_score}"

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    previewer = FormPreviewer("complex_logic_example.yaml")
    results = previewer.show_preview()
    
    # Analyze complex logic results
    income_category = results["survey"][3]["calculation"]
    eligibility_score = results["survey"][4]["calculation"]
    summary = results["survey"][5]["label"]
    
    print(f"Income category: {income_category}")
    print(f"Eligibility score: {eligibility_score}")
    print(f"Summary: {summary}")

Testing Multiple Scenarios
--------------------------

Scenario Testing Framework
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from survey123py.preview import FormPreviewer
    import yaml
    import tempfile
    import os
    
    def test_scenarios(base_yaml, scenarios):
        """Test multiple scenarios with different input values"""
        results = {}
        
        for scenario_name, test_data in scenarios.items():
            # Load base YAML
            with open(base_yaml, 'r') as f:
                survey_data = yaml.safe_load(f)
            
            # Update with test data
            for question in survey_data["survey"]:
                if question["name"] in test_data:
                    question["survey123py::preview_input"] = test_data[question["name"]]
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(survey_data, f)
                temp_file = f.name
            
            try:
                # Run preview
                previewer = FormPreviewer(temp_file)
                results[scenario_name] = previewer.show_preview()
            finally:
                # Clean up
                os.unlink(temp_file)
        
        return results

Example: Testing Age Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # age_verification.yaml
    settings:
      form_title: "Age Verification Test"
    
    survey:
      - type: integer
        name: age
        label: "Your age"
        constraint: ". >= 0 and . <= 150"
        survey123py::preview_input: 25
      
      - type: calculate
        name: age_group
        calculation: "if(${age} < 13, 'child', if(${age} < 18, 'teen', if(${age} < 65, 'adult', 'senior')))"
      
      - type: note
        name: age_status
        label: "Age group: ${age_group}"

.. code-block:: python

    # Test multiple age scenarios
    scenarios = {
        "child": {"age": 8},
        "teen": {"age": 16},
        "adult": {"age": 35},
        "senior": {"age": 70},
        "edge_teen": {"age": 17},
        "edge_adult": {"age": 18}
    }
    
    results = test_scenarios("age_verification.yaml", scenarios)
    
    # Analyze results
    for scenario, result in results.items():
        age_group = result["survey"][1]["calculation"]
        print(f"{scenario}: Age group = {age_group}")

Debugging and Validation
------------------------

Debugging Failed Tests
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from survey123py.preview import FormPreviewer
    
    def debug_preview(yaml_file):
        """Debug preview issues with detailed output"""
        try:
            previewer = FormPreviewer(yaml_file)
            results = previewer.show_preview()
            
            print("=== Survey Preview Results ===")
            for i, question in enumerate(results["survey"]):
                print(f"\nQuestion {i}: {question.get('name', 'unnamed')}")
                print(f"  Type: {question.get('type', 'unknown')}")
                print(f"  Label: {question.get('label', 'no label')}")
                
                if "survey123py::preview_input" in question:
                    print(f"  Input: {question['survey123py::preview_input']}")
                
                if "calculation" in question:
                    print(f"  Calculation: {question['calculation']}")
                
                if "constraint_result" in question:
                    status = "PASS" if question["constraint_result"] else "FAIL"
                    print(f"  Constraint: {status}")
                
                if "relevant_result" in question:
                    visibility = "VISIBLE" if question["relevant_result"] else "HIDDEN"
                    print(f"  Relevance: {visibility}")
            
            return results
            
        except Exception as e:
            print(f"Preview failed: {e}")
            import traceback
            traceback.print_exc()
            return None

Validation Helpers
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def validate_calculations(yaml_file, expected_results):
        """Validate that calculations produce expected results"""
        previewer = FormPreviewer(yaml_file)
        results = previewer.show_preview()
        
        validation_errors = []
        
        for question in results["survey"]:
            name = question.get("name")
            if name in expected_results and "calculation" in question:
                expected = expected_results[name]
                actual = question["calculation"]
                
                if actual != expected:
                    validation_errors.append(
                        f"{name}: expected {expected}, got {actual}"
                    )
        
        if validation_errors:
            print("Validation errors found:")
            for error in validation_errors:
                print(f"  - {error}")
            return False
        else:
            print("All calculations validated successfully!")
            return True
    
    # Example usage
    expected = {
        "total_score": 85.5,
        "grade": "B",
        "passed": True
    }
    
    validate_calculations("my_survey.yaml", expected)

Best Practices
--------------

1. **Comprehensive Test Data**: Include edge cases and boundary values
2. **Test All Formulas**: Verify every calculation, constraint, and relevance condition
3. **Use Realistic Data**: Test with data similar to what users will actually enter
4. **Document Test Scenarios**: Keep track of what each test validates
5. **Automate Testing**: Create scripts to run tests automatically
6. **Test Before Publishing**: Always preview before publishing to Survey123

Common Testing Patterns
----------------------

Boolean Logic Testing
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    survey:
      - type: select_one yes_no
        name: condition_a
        survey123py::preview_input: "yes"
      
      - type: select_one yes_no
        name: condition_b
        survey123py::preview_input: "no"
      
      - type: calculate
        name: both_true
        calculation: "${condition_a} = 'yes' and ${condition_b} = 'yes'"
      
      - type: calculate
        name: either_true
        calculation: "${condition_a} = 'yes' or ${condition_b} = 'yes'"

Numeric Range Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    survey:
      - type: decimal
        name: value
        survey123py::preview_input: 75.5
      
      - type: calculate
        name: in_range
        calculation: "${value} >= 50 and ${value} <= 100"
      
      - type: calculate
        name: percentage
        calculation: "${value} div 100"

String Manipulation Testing
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    survey:
      - type: text
        name: full_name
        survey123py::preview_input: "John A. Smith"
      
      - type: calculate
        name: name_length
        calculation: "string_length(${full_name})"
      
      - type: calculate
        name: has_middle_initial
        calculation: "contains(${full_name}, '.')"
      
      - type: calculate
        name: first_three_chars
        calculation: "substr(${full_name}, 0, 3)"

This comprehensive testing approach ensures your Survey123 forms work correctly before deployment and helps catch issues early in the development process.