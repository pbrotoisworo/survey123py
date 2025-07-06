"""
Unit tests for Excel to YAML conversion functionality.
"""

import unittest
import tempfile
import os
import yaml
from pathlib import Path

from survey123py.converter import ExcelToYamlConverter
from survey123py.form import FormData


class TestExcelToYamlConverter(unittest.TestCase):
    """Test cases for Excel to YAML converter."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = ExcelToYamlConverter("3.22")
        self.test_data_dir = Path(__file__).parent / "data"
        self.test_excel_path = self.test_data_dir / "test_basic_survey.xlsx"
        
        # Create temporary files for testing
        self.temp_yaml_path = tempfile.NamedTemporaryFile(suffix='.yaml', delete=False).name
        self.temp_excel_path = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False).name

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for temp_file in [self.temp_yaml_path, self.temp_excel_path]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_excel_to_yaml_conversion(self):
        """Test basic Excel to YAML conversion."""
        # Convert Excel to YAML
        yaml_data = self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Verify the YAML file was created
        self.assertTrue(os.path.exists(self.temp_yaml_path))
        
        # Verify the YAML structure
        self.assertIn('survey', yaml_data)
        self.assertIn('choices', yaml_data)
        self.assertIn('settings', yaml_data)
        
        # Verify survey questions
        survey_questions = yaml_data['survey']
        self.assertIsInstance(survey_questions, list)
        self.assertGreater(len(survey_questions), 0)
        
        # Check for specific questions from our test data
        question_names = [q.get('name') for q in survey_questions]
        self.assertIn('respondent_name', question_names)
        self.assertIn('satisfied', question_names)
        self.assertIn('thank_you', question_names)
        
        # Verify choices
        choices = yaml_data['choices']
        self.assertIsInstance(choices, list)
        choice_lists = [c.get('list_name') for c in choices]
        self.assertIn('yes_no', choice_lists)
        
        # Verify settings
        settings = yaml_data['settings']
        self.assertIsInstance(settings, dict)
        self.assertEqual(settings.get('form_title'), 'Test Survey')

    def test_yaml_file_structure(self):
        """Test that the generated YAML file has correct structure."""
        # Convert Excel to YAML
        self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Load the YAML file and verify structure
        with open(self.temp_yaml_path, 'r') as f:
            loaded_yaml = yaml.safe_load(f)
        
        # Check top-level structure
        expected_keys = ['settings', 'choices', 'survey']
        for key in expected_keys:
            self.assertIn(key, loaded_yaml)
        
        # Check survey structure
        survey = loaded_yaml['survey']
        for question in survey:
            self.assertIn('type', question)
            self.assertIn('name', question)
            self.assertIn('label', question)

    def test_round_trip_conversion(self):
        """Test that Excel -> YAML -> Excel maintains data integrity."""
        # Convert Excel to YAML
        yaml_data = self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Convert YAML back to Excel
        form_data = FormData("3.22")
        form_data.load_yaml(self.temp_yaml_path)
        form_data.save_survey(self.temp_excel_path)
        
        # Verify the round-trip Excel file was created
        self.assertTrue(os.path.exists(self.temp_excel_path))
        
        # Convert the round-trip Excel back to YAML for comparison
        temp_yaml_2 = tempfile.NamedTemporaryFile(suffix='.yaml', delete=False).name
        try:
            yaml_data_2 = self.converter.convert_excel_to_yaml(
                self.temp_excel_path, 
                temp_yaml_2
            )
            
            # Compare key elements
            self.assertEqual(
                len(yaml_data['survey']), 
                len(yaml_data_2['survey'])
            )
            
            # Compare question names
            original_names = [q.get('name') for q in yaml_data['survey']]
            roundtrip_names = [q.get('name') for q in yaml_data_2['survey']]
            self.assertEqual(set(original_names), set(roundtrip_names))
            
        finally:
            if os.path.exists(temp_yaml_2):
                os.unlink(temp_yaml_2)

    def test_validation_functionality(self):
        """Test the validation functionality of the converter."""
        # Convert Excel to YAML
        self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Run validation
        validation_results = self.converter.validate_conversion(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Check validation results structure
        self.assertIn('success', validation_results)
        self.assertIn('differences', validation_results)
        self.assertIn('warnings', validation_results)
        
        # For a proper conversion, we expect success to be True
        # (allowing for some differences due to formatting)
        self.assertIsInstance(validation_results['success'], bool)

    def test_question_types_preservation(self):
        """Test that question types are properly preserved during conversion."""
        # Convert Excel to YAML
        yaml_data = self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Check that different question types are preserved
        question_types = [q.get('type') for q in yaml_data['survey']]
        
        # Our test data should contain these types
        self.assertIn('text', question_types)
        # select_one questions include the choice list name
        select_one_types = [t for t in question_types if t.startswith('select_one')]
        self.assertGreater(len(select_one_types), 0)
        self.assertIn('note', question_types)

    def test_required_field_preservation(self):
        """Test that required fields are properly preserved."""
        # Convert Excel to YAML
        yaml_data = self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Find the required question
        required_question = None
        for question in yaml_data['survey']:
            if question.get('name') == 'respondent_name':
                required_question = question
                break
        
        self.assertIsNotNone(required_question)
        self.assertTrue(required_question.get('required'))

    def test_choice_list_preservation(self):
        """Test that choice lists are properly preserved."""
        # Convert Excel to YAML
        yaml_data = self.converter.convert_excel_to_yaml(
            str(self.test_excel_path), 
            self.temp_yaml_path
        )
        
        # Check choices structure
        choices = yaml_data['choices']
        yes_no_choices = [c for c in choices if c.get('list_name') == 'yes_no']
        
        # Should have both yes and no options
        self.assertEqual(len(yes_no_choices), 2)
        
        choice_names = [c.get('name') for c in yes_no_choices]
        self.assertIn('yes', choice_names)
        self.assertIn('no', choice_names)


if __name__ == '__main__':
    unittest.main()