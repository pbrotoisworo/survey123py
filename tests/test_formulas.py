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

    def test_jr_choice_name(self):
        tpl = self.tpl.copy()
        val1 = "'option2'"  # Choice value (quoted)
        val2 = "test_options"  # List name (unquoted since it will be quoted in the formula)

        tpl["choices"] = [
            {"list_name": "test_options", "name": "option1", "label": "Option 1"},
            {"list_name": "test_options", "name": "option2", "label": "Option 2"},
            {"list_name": "test_options", "name": "option3", "label": "Option 3"}
        ]

        tpl["survey"] = [
            {
                "type": "select_one test_options",
                "name": "q1",
                "label": "Single select question",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "List name",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Choice Name Calculation",
                "calculation": "jr:choice-name(${q1}, '${q2}')",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Choice name result is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Since this is a simplified implementation, it returns the choice_value
        self.assertEqual(results["survey"][2]["calculation"], "option2", msg="jr_choice_name calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_jr_choice_name_empty(self):
        """Test jr_choice_name with empty inputs"""
        from survey123py.formulas import jr_choice_name
        
        # Test with empty choice value
        self.assertEqual(jr_choice_name("", "test_list"), "")
        
        # Test with None choice value
        self.assertEqual(jr_choice_name(None, "test_list"), "")
        
        # Test with valid choice value
        self.assertEqual(jr_choice_name("option1", "test_list"), "option1")

    def test_boolean(self):
        tpl = self.tpl.copy()
        
        test_cases = [
            (1, True),
            (0, False),
            ("true", True),
            ("false", False),
            ("yes", True),
            ("no", False),
            ("", False)
        ]
        
        for i, (input_val, expected) in enumerate(test_cases):
            tpl["survey"] = [
                {
                    "type": "text",
                    "name": "q1",
                    "label": f"Test input {i}",
                    "survey123py::preview_input": input_val
                },
                {
                    "type": "text",
                    "name": "outputCalculation",
                    "label": "Boolean Calculation",
                    "calculation": "boolean(${q1})",
                },
            ]

            with open(self.test_tmp_file, 'w') as file:
                yaml.dump(tpl, file)
            
            preview = FormPreviewer(str(self.test_tmp_file))
            results = preview.show_preview()
            
            self.assertEqual(results["survey"][1]["calculation"], expected, 
                           msg=f"boolean({input_val}) should return {expected}")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_coalesce(self):
        tpl = self.tpl.copy()
        val1 = ""  # Empty value
        val2 = "backup_value"  # Non-empty backup
        val3 = "default"  # Default value

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Primary value",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Backup value",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "q3",
                "label": "Default value",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Coalesce Calculation",
                "calculation": "coalesce(${q1}, ${q2}, ${q3})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][3]["calculation"], "backup_value", 
                        msg="coalesce should return first non-empty value")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_count(self):
        tpl = self.tpl.copy()
        val1 = "value1"
        val2 = ""  # Empty
        val3 = "value3"

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Field 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Field 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "q3",
                "label": "Field 3",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Count Calculation",
                "calculation": "count(${q1}, ${q2}, ${q3})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][3]["calculation"], 2, 
                        msg="count should return 2 for two non-empty values")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_count_selected(self):
        tpl = self.tpl.copy()
        val1 = "'option1,option3,option5'"  # Multi-select with 3 selections

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
                "name": "outputCalculation",
                "label": "Count Selected Calculation",
                "calculation": "count-selected(${q1})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][1]["calculation"], 3, 
                        msg="count-selected should return 3 for three selections")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_date_time(self):
        tpl = self.tpl.copy()
        val1 = "'2024-06-14T10:30:00'"  # ISO datetime format

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "DateTime input",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "DateTime Calculation",
                "calculation": "date-time(${q1})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should return a timestamp in milliseconds
        self.assertIsInstance(results["survey"][1]["calculation"], int, 
                             msg="date-time should return integer timestamp")
        self.assertGreater(results["survey"][1]["calculation"], 0, 
                          msg="date-time should return positive timestamp")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_decimal_date_time(self):
        tpl = self.tpl.copy()
        val1 = 1718371200000  # Timestamp in milliseconds (June 14, 2024)

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Timestamp input",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Decimal DateTime Calculation",
                "calculation": "decimal-date-time(${q1})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should return a decimal number representing days since Excel epoch
        self.assertIsInstance(results["survey"][1]["calculation"], float, 
                             msg="decimal-date-time should return float")
        self.assertGreater(results["survey"][1]["calculation"], 40000, 
                          msg="decimal-date-time should return reasonable date value")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_new_functions_error_handling(self):
        """Test error handling for new functions"""
        from survey123py.formulas import boolean, coalesce, count, count_selected, date_time, decimal_date_time
        
        # Test boolean with various inputs
        self.assertEqual(boolean(None), False)
        self.assertEqual(boolean(""), False)
        self.assertEqual(boolean(0), False)
        self.assertEqual(boolean(1), True)
        
        # Test coalesce with all empty values
        self.assertEqual(coalesce("", None, ""), "")
        
        # Test count with all empty values
        self.assertEqual(count("", None, ""), 0)
        
        # Test count_selected with empty input
        self.assertEqual(count_selected(""), 0)
        self.assertEqual(count_selected(None), 0)
        
        # Test date_time with invalid format
        with self.assertRaises(ValueError):
            date_time("invalid-date")
        
        # Test decimal_date_time with invalid input
        with self.assertRaises(ValueError):
            decimal_date_time("invalid")

    def test_false(self):
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "False Calculation",
                "calculation": "false()",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["calculation"], False, 
                        msg="false() should return False")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_join(self):
        tpl = self.tpl.copy()
        val1 = "Apple"
        val2 = "Orange"
        val3 = ""  # Empty value (should be excluded)
        separator = " - "

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Field 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "q2",
                "label": "Field 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "text",
                "name": "q3",
                "label": "Field 3",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Join Calculation",
                "calculation": f"join('{separator}', ${'{q1}'}, ${'{q2}'}, ${'{q3}'})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][3]["calculation"], "Apple - Orange", 
                        msg="join should concatenate non-empty values with separator")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_max(self):
        tpl = self.tpl.copy()
        val1 = 10
        val2 = 5
        val3 = 15

        tpl["survey"] = [
            {
                "type": "integer",
                "name": "q1",
                "label": "Number 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "integer",
                "name": "q2",
                "label": "Number 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "integer",
                "name": "q3",
                "label": "Number 3",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Max Calculation",
                "calculation": "max(${q1}, ${q2}, ${q3})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][3]["calculation"], 15.0, 
                        msg="max should return the largest value")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_min(self):
        tpl = self.tpl.copy()
        val1 = 10
        val2 = 5
        val3 = 15

        tpl["survey"] = [
            {
                "type": "integer",
                "name": "q1",
                "label": "Number 1",
                "survey123py::preview_input": val1
            },
            {
                "type": "integer",
                "name": "q2",
                "label": "Number 2",
                "survey123py::preview_input": val2
            },
            {
                "type": "integer",
                "name": "q3",
                "label": "Number 3",
                "survey123py::preview_input": val3
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Min Calculation",
                "calculation": "min(${q1}, ${q2}, ${q3})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][3]["calculation"], 5.0, 
                        msg="min should return the smallest value")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_not(self):
        tpl = self.tpl.copy()
        val1 = True

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Boolean value",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Not Calculation",
                "calculation": "not(${q1})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][1]["calculation"], False, 
                        msg="not(True) should return False")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_now(self):
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Now Calculation",
                "calculation": "now()",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should return a timestamp in milliseconds (positive integer)
        self.assertIsInstance(results["survey"][0]["calculation"], int, 
                             msg="now() should return integer timestamp")
        self.assertGreater(results["survey"][0]["calculation"], 0, 
                          msg="now() should return positive timestamp")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_number(self):
        tpl = self.tpl.copy()
        val1 = "123.45"  # String that can be converted to number

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Text field with number",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Number Calculation",
                "calculation": "number(${q1})",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][1]["calculation"], 123.45, 
                        msg="number should convert string to float")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_additional_functions_error_handling(self):
        """Test error handling for additional functions"""
        from survey123py.formulas import false, join, max, min, not_, now, number
        
        # Test false (no arguments)
        self.assertEqual(false(), False)
        
        # Test join with empty values
        self.assertEqual(join("-", "", None, "value"), "value")
        
        # Test max/min with no valid numeric values
        self.assertEqual(max("text", "", None), None)
        self.assertEqual(min("text", "", None), None)
        
        # Test max/min with mixed numeric and non-numeric
        self.assertEqual(max(1, "text", 3, ""), 3.0)
        self.assertEqual(min(1, "text", 3, ""), 1.0)
        
        # Test not_ with various values
        self.assertEqual(not_(True), False)
        self.assertEqual(not_(False), True)
        self.assertEqual(not_(1), False)
        self.assertEqual(not_(0), True)
        self.assertEqual(not_(""), True)
        
        # Test now returns reasonable timestamp
        timestamp = now()
        self.assertIsInstance(timestamp, int)
        self.assertGreater(timestamp, 1600000000000)  # After 2020
        
        # Test number with invalid input
        self.assertEqual(number("invalid"), None)
        self.assertEqual(number(""), None)
        self.assertEqual(number(None), None)

    def test_dot_operator_in_constraint_with_numbers(self):
        """Test dot operator in constraints with numeric fields"""
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "integer",
                "name": "num_field",
                "label": "Number field (must be > 5)",
                "survey123py::preview_input": 8,
                "constraint": ". > 5",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["constraint_result"], True, 
                        msg="Constraint with dot operator: 8 > 5 should be True")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_dot_operator_in_constraint_with_strings(self):
        """Test dot operator in constraints with string fields"""
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "text",
                "name": "text_field",
                "label": "Text field",
                "survey123py::preview_input": "hello",
                "constraint": "string_length(.) >= 3",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["constraint_result"], True, 
                        msg="String constraint with dot operator: length of 'hello' >= 3 should be True")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_dot_operator_constraint_false_condition(self):
        """Test dot operator in constraints that evaluate to false"""
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "integer",
                "name": "num_field",
                "label": "Number field (must be < 10)",
                "survey123py::preview_input": 15,
                "constraint": ". < 10",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["constraint_result"], False, 
                        msg="Constraint with dot operator: 15 < 10 should be False")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_dot_operator_with_decimals_in_constraint(self):
        """Test that dot operator doesn't interfere with decimal numbers in constraints"""
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "decimal",
                "name": "decimal_field",
                "label": "Decimal field",
                "survey123py::preview_input": 7.5,
                "constraint": ". >= 2.5 and . <= 10.0",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should be: 7.5 >= 2.5 and 7.5 <= 10.0 = True
        self.assertEqual(results["survey"][0]["constraint_result"], True, 
                        msg="Constraint with decimals: 7.5 >= 2.5 and 7.5 <= 10.0 should be True")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_dot_operator_constraint_with_mixed_expressions(self):
        """Test dot operator in constraints with mixed expressions including variables"""
        tpl = self.tpl.copy()

        tpl["survey"] = [
            {
                "type": "integer",
                "name": "min_value",
                "label": "Minimum value",
                "survey123py::preview_input": 5
            },
            {
                "type": "integer",
                "name": "current_field",
                "label": "Current field",
                "survey123py::preview_input": 10,
                "constraint": ". >= ${min_value}",
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should be: 10 >= 5 = True
        self.assertEqual(results["survey"][1]["constraint_result"], True, 
                        msg="Mixed constraint expression: 10 >= 5 should be True")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_version(self):
        """Test version function returns settings version"""
        tpl = self.tpl.copy()
        tpl["settings"]["version"] = "1.2.3"
        tpl["survey"] = [
            {
                "type": "text",
                "name": "version_field",
                "label": "Version",
                "calculation": "version()",
                "survey123py::preview_input": "",  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["calculation"], "1.2.3", 
                        msg="Version should return settings version value")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_version_no_settings(self):
        """Test version function with no version in settings"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "text",
                "name": "version_field",
                "label": "Version",
                "calculation": "version()",
                "survey123py::preview_input": "",  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][0]["calculation"], "", 
                        msg="Version should return empty string when no version in settings")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_uuid(self):
        """Test uuid function generates valid UUID"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "text",
                "name": "uuid_field",
                "label": "UUID",
                "calculation": "uuid()",
                "survey123py::preview_input": "",  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        uuid_result = results["survey"][0]["calculation"]
        # Basic UUID format check (8-4-4-4-12 characters)
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        self.assertTrue(re.match(uuid_pattern, uuid_result), 
                       msg=f"UUID should match standard format, got: {uuid_result}")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_today(self):
        """Test today function returns today's date as timestamp"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "integer",
                "name": "today_field",
                "label": "Today",
                "calculation": "today()",
                "survey123py::preview_input": 0,  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        today_result = results["survey"][0]["calculation"]
        # Should be an integer timestamp
        self.assertIsInstance(today_result, int, 
                             msg="Today should return integer timestamp")
        # Should be reasonable timestamp (after 2020 and before 2030)
        from datetime import datetime
        min_timestamp = int(datetime(2020, 1, 1).timestamp() * 1000)
        max_timestamp = int(datetime(2030, 1, 1).timestamp() * 1000)
        self.assertTrue(min_timestamp < today_result < max_timestamp,
                       msg=f"Today timestamp should be reasonable, got: {today_result}")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_sum(self):
        """Test sum function with multiple arguments"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "integer",
                "name": "num1",
                "label": "Number 1",
                "survey123py::preview_input": 5
            },
            {
                "type": "integer", 
                "name": "num2",
                "label": "Number 2",
                "survey123py::preview_input": 10
            },
            {
                "type": "text",
                "name": "non_numeric",
                "label": "Non-numeric",
                "survey123py::preview_input": "hello"
            },
            {
                "type": "decimal",
                "name": "sum_field",
                "label": "Sum",
                "calculation": "sum(${num1}, ${num2}, ${non_numeric}, 2.5)",
                "survey123py::preview_input": 0,  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        # Should sum: 5 + 10 + 2.5 = 17.5 (non_numeric "hello" is ignored)
        self.assertEqual(results["survey"][3]["calculation"], 17.5, 
                        msg="Sum should add numeric values and ignore non-numeric")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_regex(self):
        """Test regex function pattern matching"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "text",
                "name": "phone",
                "label": "Phone",
                "survey123py::preview_input": "123-456-7890"
            },
            {
                "type": "text",
                "name": "email",
                "label": "Email", 
                "survey123py::preview_input": "test@example.com"
            },
            {
                "type": "text",
                "name": "phone_check",
                "label": "Phone Check",
                "calculation": "regex('[0-9]{3}-[0-9]{3}-[0-9]{4}', ${phone})",
                "survey123py::preview_input": "",  # Placeholder value
            },
            {
                "type": "text",
                "name": "email_check",
                "label": "Email Check",
                "calculation": "regex('@', ${email})",
                "survey123py::preview_input": "",  # Placeholder value
            },
            {
                "type": "text",
                "name": "invalid_check",
                "label": "Invalid Check",
                "calculation": "regex('[0-9]+', 'abc')",
                "survey123py::preview_input": "",  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertEqual(results["survey"][2]["calculation"], True, 
                        msg="Phone regex should match")
        self.assertEqual(results["survey"][3]["calculation"], True, 
                        msg="Email regex should match @ symbol")
        self.assertEqual(results["survey"][4]["calculation"], False, 
                        msg="Invalid regex should not match numbers in 'abc'")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_random(self):
        """Test random function returns value between 0 and 1"""
        tpl = self.tpl.copy()
        tpl["survey"] = [
            {
                "type": "decimal",
                "name": "random_field",
                "label": "Random",
                "calculation": "random()",
                "survey123py::preview_input": 0,  # Placeholder value
            },
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        random_result = results["survey"][0]["calculation"]
        self.assertIsInstance(random_result, float, 
                             msg="Random should return float")
        self.assertTrue(0 <= random_result < 1, 
                       msg=f"Random should be between 0 and 1, got: {random_result}")

        # Cleanup
        os.remove(self.test_tmp_file)

    def test_new_formulas_error_handling(self):
        """Test error handling for new formulas"""
        from survey123py.formulas import regex, sum
        
        # Test regex with invalid pattern
        self.assertEqual(regex("[invalid", "test"), False, 
                        msg="Invalid regex pattern should return False")
        
        # Test sum with empty args
        self.assertEqual(sum(), 0, 
                        msg="Sum with no args should return 0")
        
        # Test sum with all non-numeric
        self.assertEqual(sum("abc", "def", None), 0, 
                        msg="Sum with all non-numeric should return 0")

