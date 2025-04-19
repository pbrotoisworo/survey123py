import unittest
from pathlib import Path
from survey123py.form import FormData

class TestSurvey123_322(unittest.TestCase):

    def setUp(self):
        self.survey = FormData("3.22")
        self.test_file = Path(__file__).parent / "data" / "sample_survey_full.yaml"

    def test_load_survey(self):
        self.survey.load_yaml(self.test_file)

    def test_save_survey(self):
        self.survey.load_yaml(self.test_file)
        self.survey.save_survey("output.xlsx")

if __name__ == "__main__":
    unittest.main()