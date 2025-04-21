import unittest
from pathlib import Path
from survey123py.form import FormData, Sheets
import pandas as pd

class TestSurvey123_322(unittest.TestCase):

    def setUp(self):
        self.survey = FormData("3.22")
        self.test_file = Path(__file__).parent / "data" / "sample_survey_full.yaml"
        self.sheet_names = Sheets

    def test_load_survey(self):
        
        self.survey.load_yaml(self.test_file)

        # All data from template and YAML must be loaded into a dataframe
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.survey], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.survey])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.choices], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.choices])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.settings], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.settings])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.version], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.version])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.question_types], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.question_types])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.appearances], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.appearances])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.field_types], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.field_types])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.reference], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.reference])}")
        self.assertTrue(isinstance(self.survey.sheets[self.sheet_names.reserved], pd.DataFrame), f"Expecting pd.DataFrame. Got {type(self.survey.sheets[self.sheet_names.reserved])}")

        # TODO: Verify dataframe values


    def test_save_survey(self):
        self.survey.load_yaml(self.test_file)
        self.survey.save_survey("output.xlsx")

if __name__ == "__main__":
    unittest.main()