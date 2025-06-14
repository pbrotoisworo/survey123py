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

    def format_date(self):
        tpl = self.tpl.copy()
        val1 = 1718371200000
        val1_formatted = "2023-10-01"

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

