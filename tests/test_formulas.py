import unittest
from survey123py.form import FormData, Sheets
from survey123py.preview import FormPreviewer
from pathlib import Path
import yaml
import os

def generate_test_survey(formula: str, input_value: any):
    """
    Used to quickly generate a test survey for math formulas.
    """
    return [
            {
                "type": "text",
                "name": "q1",
                "label": "Input for math calculation",
                "survey123py::preview_input": input_value
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Acos Calculation",
                "calculation": formula + "(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Math output is: ${outputCalculation}",
            }
        ]


class TestSurvey123_322_Preview(unittest.TestCase):

    def setUp(self):
        self.survey = FormData("3.22")
        self.test_file = Path(__file__).parent / "data" / "sample_survey_formulas.yaml"
        self.test_tmp_file = Path(__file__).parent / "data" / "test_tmp_input.yaml"
        # self.test_tmpout_file = Path(__file__).parent / "data" / "test_tmp_output.yaml"
        self.preview = FormPreviewer(str(self.test_file))
        self.sheet_names = Sheets

        self.tpl = {"settings": {"form_title": "Test Form"}, "survey": []}

    def test_nested_formula(self):

        tpl = self.tpl.copy()
        val1 = "Apple"
        val2 = "Red"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "What is your favorite color?",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Nested Calculation",
                "calculation": "contains(concat(${q1}, ' and ', ${q2}), 'Apple')",
            },
            {
                "type": "text",
                "name": "outputCalculation2",
                "label": "Nested Calculation2",
                "calculation": "contains(concat(${q1}, ' and ', ${q2}), 'Orange')",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Nested Output is: ${outputCalculation}",
            },
            {
                "type": "note",
                "name": "output2",
                "label": "Nested Output is: ${outputCalculation2}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][4]["label"], f"Nested Output is: True", "Label not parsed correctly")
        self.assertAlmostEqual(results["survey"][5]["label"], f"Nested Output is: False", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_if(self):
        tpl = self.tpl.copy()
        val1 = "Apple"
        val2 = "Red"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "What is your favorite color?",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "If Calculation",
                "calculation": "if(contains(${q1}, 'Apple'), 'Yep', 'Nope')",
            },
            {
                "type": "note",
                "name": "output",
                "label": "If Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][3]["label"], f"If Output is: Yep", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_int(self):
        tpl = self.tpl.copy()
        val1 = 42

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Input for integer conversion",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Integer Conversion Calculation",
                "calculation": "int(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Integer Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Integer Output is: 42", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_boolean_from_string(self):
        tpl = self.tpl.copy()
        val1 = "true"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Input for boolean conversion",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Boolean Conversion Calculation",
                "calculation": "boolean_from_string(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Boolean Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Boolean Output is: True", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_date(self):
        tpl = self.tpl.copy()
        val1 = "2017-05-28"
        val1_ts = 1495900800000

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Input Date",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Date Calculation",
                "calculation": "date(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Date Output is: ${outputCalculation}",
            }
        ]
        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Date Output is: {val1_ts}", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_format_date(self):
        tpl = self.tpl.copy()
        val1 = 1718371200000
        val1_formatted = "2024-06-14"

        tpl["survey"] = [
            {
                "type": "date",
                "name": "q1",
                "label": "Input Date",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Format Date Calculation",
                "calculation": "format-date(${q1}, '%Y-%m-%d')",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Formatted Date Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Formatted Date Output is: {val1_formatted}", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_starts_with(self):
        tpl = self.tpl.copy()
        val1 = "Apple"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Starts With Calculation",
                "calculation": "starts-with(${q1}, 'App')",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Starts With Output is: ${outputCalculation}",
            }
        ]
        
        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Starts With Output is: True", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_string_length(self):
        tpl = self.tpl.copy()
        val1 = "Apple"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "String Length Calculation",
                "calculation": "string_length(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "String Length Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"String Length Output is: 5", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_string(self):
        tpl = self.tpl.copy()
        val1 = 12345

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite number?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "String Conversion Calculation",
                "calculation": "string(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "String Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"String Output is: 12345", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_substr(self):
        tpl = self.tpl.copy()
        val1 = "Apple"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Substring Calculation",
                "calculation": "substr(${q1}, 1, 3)",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Substring Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][2]["label"], f"Substring Output is: ppl", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_concat(self):
        tpl = self.tpl.copy()
        val1 = "Apple"
        val2 = "Red"
        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "What is your favorite fruit?",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "What is your favorite color?",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Concat Calculation",
                "calculation": "concat(${q1}, ' and ', ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Concat Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        self.assertEqual(results["survey"][3]["label"], f"Concat Output is: {val1} and {val2}", "Label not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_acos(self):
        tpl = self.tpl.copy()
        input_value = 0.5

        tpl["survey"] = generate_test_survey("acos", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 1.0471975511965979, 5, msg="acos calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_cos(self):
        tpl = self.tpl.copy()
        input_value = 0.34
        
        tpl["survey"] = generate_test_survey("cos", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 0.9427546655283462, 5, msg="cos calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_sin(self):
        tpl = self.tpl.copy()
        input_value = 1.5

        tpl["survey"] = generate_test_survey("sin", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 0.9974949866040544, 5, msg="sin calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)
    
    def test_asin(self):
        tpl = self.tpl.copy()
        input_value = 0.56

        tpl["survey"] = generate_test_survey("asin", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 0.5943858000010622, 5, msg="asin calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)
    
    def test_atan(self):
        tpl = self.tpl.copy()
        input_value = 1.5

        tpl["survey"] = generate_test_survey("atan", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 0.9827937232473292, 5, msg="atan calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)
    
    def test_atan2(self):
        tpl = self.tpl.copy()
        val1 = 3.0  # y value
        val2 = 4.0  # x value

        tpl["survey"] = [
            {
                "type": "decimal",
                "name": "q1",
                "label": "Y coordinate",
                "survey123py::preview_input": val1
            },
            {
                "type": "decimal", 
                "name": "q2",
                "label": "X coordinate",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Atan2 Calculation",
                "calculation": "atan2(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Math output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][2]["calculation"], 0.6435011087932844, 5, msg="atan2 calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)
    
    def test_and_operator(self):
        tpl = self.tpl.copy()
        val1 = True
        val2 = False

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Boolean value 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "text", 
                "name": "q2",
                "label": "Boolean value 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "result_true_false",
                "label": "And operation result",
                "calculation": "${q1} and ${q2}",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Result is: ${result_true_false}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], False, msg="and operator not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_or_operator(self):
        tpl = self.tpl.copy()
        val1 = True
        val2 = False

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Boolean value 1", 
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2", 
                "label": "Boolean value 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "result_true_false",
                "label": "Or operation result",
                "calculation": "${q1} or ${q2}",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Result is: ${result_true_false}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], True, msg="or operator not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_and_or_combined(self):
        tpl = self.tpl.copy()
        val1 = True
        val2 = False
        val3 = True

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Boolean value 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Boolean value 2", 
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "q3",
                "label": "Boolean value 3",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "result_combined",
                "label": "Combined and/or operation result",
                "calculation": "(${q1} and ${q2}) or ${q3}",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Result is: ${result_combined}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # (True and False) or True = False or True = True
        self.assertEqual(results["survey"][3]["calculation"], True, msg="combined and/or operator not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_tan(self):
        tpl = self.tpl.copy()
        input_value = 0.785398  # π/4 radians

        tpl["survey"] = generate_test_survey("tan", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 1.0000003465725653, 5, msg="tan calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_exp(self):
        tpl = self.tpl.copy()
        input_value = 2.0

        tpl["survey"] = generate_test_survey("exp", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 7.38905609893065, 5, msg="exp calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_exp10(self):
        tpl = self.tpl.copy()
        input_value = 3.0

        tpl["survey"] = generate_test_survey("exp10", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 1000.0, 5, msg="exp10 calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_log(self):
        tpl = self.tpl.copy()
        input_value = 2.71828  # approximately e

        tpl["survey"] = generate_test_survey("log", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 0.9999986932206651, 5, msg="log calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_log10(self):
        tpl = self.tpl.copy()
        input_value = 1000.0

        tpl["survey"] = generate_test_survey("log10", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 3.0, 5, msg="log10 calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_log_error_handling(self):
        """Test that log functions raise ValueError for non-positive values"""
        from survey123py.formulas import log, log10
        
        with self.assertRaises(ValueError):
            log(0)
        
        with self.assertRaises(ValueError):
            log(-1)
            
        with self.assertRaises(ValueError):
            log10(0)
            
        with self.assertRaises(ValueError):
            log10(-1)

    def test_pi(self):
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Pi Calculation",
                "calculation": "pi()",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Pi value is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][0]["calculation"], 3.141592653589793, 5, msg="pi calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_pow(self):
        tpl = self.tpl.copy()
        val1 = 2.0
        val2 = 3.0

        tpl["survey"] = [
            {
                "type": "decimal",
                "name": "q1",
                "label": "Base value",
                "survey123py::preview_input": val1
            },
            {
                "type": "decimal", 
                "name": "q2",
                "label": "Exponent value",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Power Calculation",
                "calculation": "pow(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Power result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][2]["calculation"], 8.0, 5, msg="pow calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_round(self):
        tpl = self.tpl.copy()
        input_value = 3.14159

        tpl["survey"] = generate_test_survey("round", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][1]["calculation"], 3.0, msg="round calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_round_with_digits(self):
        tpl = self.tpl.copy()
        val1 = 3.14159
        val2 = 2

        tpl["survey"] = [
            {
                "type": "decimal",
                "name": "q1",
                "label": "Value to round",
                "survey123py::preview_input": val1
            },
            {
                "type": "integer",
                "name": "q2",
                "label": "Number of digits",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Round Calculation",
                "calculation": "round(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Rounded result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], 3.14, msg="round with digits calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_sqrt(self):
        tpl = self.tpl.copy()
        input_value = 16.0

        tpl["survey"] = generate_test_survey("sqrt", input_value)

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 4.0, 5, msg="sqrt calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_sqrt_error_handling(self):
        """Test that sqrt raises ValueError for negative values"""
        from survey123py.formulas import sqrt
        
        with self.assertRaises(ValueError):
            sqrt(-1)

    def test_selected(self):
        tpl = self.tpl.copy()
        val1 = "'option1,option3,option5'"  # Multi-select answer (comma-separated, quoted)
        val2 = "option3"  # Choice to check

        tpl["choices"] = [
            {"list_name": "test_options", "name": "option1", "label": "Option 1"},
            {"list_name": "test_options", "name": "option2", "label": "Option 2"},
            {"list_name": "test_options", "name": "option3", "label": "Option 3"},
            {"list_name": "test_options", "name": "option4", "label": "Option 4"},
            {"list_name": "test_options", "name": "option5", "label": "Option 5"}
        ]

        tpl["survey"] = [
            {
                "type": "select_multiple test_options",
                "name": "q1",
                "label": "Multi-select question",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Choice to check",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Selected Calculation",
                "calculation": "selected(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Selected result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], True, msg="selected calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_selected_false(self):
        tpl = self.tpl.copy()
        val1 = "'option1,option3,option5'"  # Multi-select answer (comma-separated, quoted)
        val2 = "option2"  # Choice to check (not selected)

        tpl["choices"] = [
            {"list_name": "test_options", "name": "option1", "label": "Option 1"},
            {"list_name": "test_options", "name": "option2", "label": "Option 2"},
            {"list_name": "test_options", "name": "option3", "label": "Option 3"},
            {"list_name": "test_options", "name": "option4", "label": "Option 4"},
            {"list_name": "test_options", "name": "option5", "label": "Option 5"}
        ]

        tpl["survey"] = [
            {
                "type": "select_multiple test_options",
                "name": "q1",
                "label": "Multi-select question",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Choice to check",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Selected Calculation",
                "calculation": "selected(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Selected result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], False, msg="selected calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_selected_at(self):
        tpl = self.tpl.copy()
        val1 = "'option1,option3,option5'"  # Multi-select answer (comma-separated, quoted)
        val2 = 1  # Index to get

        tpl["choices"] = [
            {"list_name": "test_options", "name": "option1", "label": "Option 1"},
            {"list_name": "test_options", "name": "option2", "label": "Option 2"},
            {"list_name": "test_options", "name": "option3", "label": "Option 3"},
            {"list_name": "test_options", "name": "option4", "label": "Option 4"},
            {"list_name": "test_options", "name": "option5", "label": "Option 5"}
        ]

        tpl["survey"] = [
            {
                "type": "select_multiple test_options",
                "name": "q1",
                "label": "Multi-select question",
                "survey123py::preview_input": val1
            },
            {
                "type": "integer",
                "name": "q2",
                "label": "Index to get",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Selected At Calculation",
                "calculation": "selected_at(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Selected at result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], "option3", msg="selected_at calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_selected_at_out_of_bounds(self):
        tpl = self.tpl.copy()
        val1 = "'option1,option3'"  # Multi-select answer with 2 items (comma-separated, quoted)
        val2 = 5  # Index out of bounds

        tpl["choices"] = [
            {"list_name": "test_options", "name": "option1", "label": "Option 1"},
            {"list_name": "test_options", "name": "option2", "label": "Option 2"},
            {"list_name": "test_options", "name": "option3", "label": "Option 3"}
        ]

        tpl["survey"] = [
            {
                "type": "select_multiple test_options",
                "name": "q1",
                "label": "Multi-select question",
                "survey123py::preview_input": val1
            },
            {
                "type": "integer",
                "name": "q2",
                "label": "Index to get",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Selected At Calculation",
                "calculation": "selected_at(${q1}, ${q2})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Selected at result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], "", msg="selected_at out of bounds calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_selected_empty_inputs(self):
        """Test selected functions with empty inputs"""
        from survey123py.formulas import selected, selected_at
        
        # Test selected with empty inputs
        self.assertEqual(selected("", "option1"), False)
        self.assertEqual(selected("option1,option2", ""), False)
        self.assertEqual(selected("", ""), False)
        
        # Test selected_at with empty inputs
        self.assertEqual(selected_at("", 0), "")
        self.assertEqual(selected_at("option1,option2", -1), "")
        self.assertEqual(selected_at("option1,option2", 10), "")

