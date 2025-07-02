import unittest
from survey123py.form import FormData, Sheets
from survey123py.preview import FormPreviewer
from pathlib import Path


class TestSurvey123_322_Preview(unittest.TestCase):

    def setUp(self):
        self.survey = FormData("3.22")
        self.test_file = Path(__file__).parent / "data" / "sample_survey_parsing.yaml"
        self.test_file_error = Path(__file__).parent / "data" / "sample_survey_parsing_error.yaml"
        self.preview = FormPreviewer(str(self.test_file))
        self.preview_error = FormPreviewer(str(self.test_file_error))
        self.sheet_names = Sheets

    def test_valid_parsing(self):

        # Test parsing a valid survey file
        # ${q1} is "John Doe"
        # ${q2} is "30"
        output_yaml = self.preview.show_preview()
        self.assertEqual(output_yaml["survey"][2]["label"], "Personal Data (John Doe)", "Label not parsed correctly")
        self.assertEqual(output_yaml["survey"][2]["children"][0]["label"], "Nationality of John Doe. Age 30", "Label not parsed correctly")
        self.assertEqual(output_yaml["survey"][3]["label"], "The answers are John Doe and 30", "Label not parsed correctly")      

    def test_invalid_parsing(self):
        # Test parsing an invalid survey file
        # It should raise a value error due to ${} variable not found in the context
        with self.assertRaises(ValueError) as context:
            self.preview_error.show_preview()