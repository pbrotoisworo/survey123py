import unittest
from survey123py.form import FormData, Sheets
from survey123py.preview import FormPreviewer
from pathlib import Path
import yaml
import os


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
        val1 = 0.5

        tpl["survey"] = [
            {
                "type": "text",
                "name": "q1",
                "label": "Input for arc cosine calculation",
                "survey123py::preview_input": val1
            },
            {
                "type": "text",
                "name": "outputCalculation",
                "label": "Acos Calculation",
                "calculation": "acos(${q1})",
            },
            {
                "type": "note",
                "name": "output",
                "label": "Acos Output is: ${outputCalculation}",
            }
        ]

        with open(self.test_tmp_file, 'w') as file:
            yaml.dump(tpl, file)
        
        preview = FormPreviewer(str(self.test_tmp_file))
        results = preview.show_preview()
        
        self.assertAlmostEqual(results["survey"][1]["calculation"], 1.0471975511965979, 5, msg="acos calculation not parsed correctly")

        # Cleanup
        os.remove(self.test_tmp_file)
         

