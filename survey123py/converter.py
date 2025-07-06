"""
Excel to YAML Converter Module

This module provides functionality to convert Survey123-compatible Excel files
back to YAML format, enabling round-trip conversion and migration of existing surveys.
"""

import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import warnings

from .form import FormData, Sheets


class ExcelToYamlConverter:
    """
    Converter class for converting Survey123 Excel files to YAML format.
    
    This enables round-trip conversion and migration of existing Survey123 forms
    created in Survey123 Connect or other tools.
    """
    
    def __init__(self, version: str = "3.22"):
        """
        Initialize the converter.
        
        Parameters
        ----------
        version : str, optional
            Survey123 version to use for column mappings, by default "3.22"
        """
        self.version = version
        self.form_data = FormData(version)
        
        # Load column mappings for reverse conversion
        template_path = Path(__file__).parent / "template" / f"template_{version}_columns.json"
        with open(template_path, 'r') as f:
            self.column_mappings = json.load(f)
        
        # Create reverse mappings (Excel column -> YAML field)
        self.reverse_mappings = {}
        for sheet_name, mappings in self.column_mappings.items():
            self.reverse_mappings[sheet_name] = {v: k for k, v in mappings.items()}
    
    def convert_excel_to_yaml(self, excel_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert a Survey123 Excel file to YAML format.
        
        Parameters
        ----------
        excel_path : str
            Path to the Survey123 Excel file
        output_path : str, optional
            Path to save the YAML file. If None, returns the data without saving
        
        Returns
        -------
        Dict[str, Any]
            The survey data in YAML-compatible format
        
        Raises
        ------
        FileNotFoundError
            If the Excel file doesn't exist
        ValueError
            If the Excel file is not a valid Survey123 format
        """
        if not Path(excel_path).exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        # Read Excel file
        try:
            excel_data = pd.read_excel(excel_path, sheet_name=None, dtype=str)
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")
        
        # Initialize YAML structure
        yaml_data = {}
        
        # Convert each sheet
        sheets = Sheets()
        
        if sheets.survey in excel_data:
            yaml_data['survey'] = self._convert_survey_sheet(excel_data[sheets.survey])
        
        if sheets.choices in excel_data:
            yaml_data['choices'] = self._convert_choices_sheet(excel_data[sheets.choices])
        
        if sheets.settings in excel_data:
            yaml_data['settings'] = self._convert_settings_sheet(excel_data[sheets.settings])
        
        # Save to file if output path provided
        if output_path:
            self._save_yaml(yaml_data, output_path)
        
        return yaml_data
    
    def _convert_survey_sheet(self, survey_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert the survey sheet to YAML format."""
        survey_questions = []
        
        # Get reverse mappings for survey sheet
        sheets = Sheets()
        reverse_map = self.reverse_mappings.get(sheets.survey, {})
        
        for _, row in survey_df.iterrows():
            question = {}
            
            # Convert each column using reverse mappings
            for excel_col, value in row.items():
                if pd.isna(value) or value == '':
                    continue
                
                # Map Excel column to YAML field
                yaml_field = reverse_map.get(excel_col, excel_col.lower().replace(' ', '_'))
                
                # Handle special cases
                if yaml_field == 'type':
                    question[yaml_field] = self._clean_type_value(value)
                elif yaml_field in ['required', 'readonly']:
                    question[yaml_field] = self._convert_yes_no_to_bool(value)
                elif yaml_field in ['children']:
                    # Skip children for now - handle in post-processing
                    continue
                else:
                    question[yaml_field] = str(value).strip()
            
            if question:  # Only add non-empty questions
                survey_questions.append(question)
        
        # Post-process to handle groups and repeats
        return self._process_groups_and_repeats(survey_questions)
    
    def _convert_choices_sheet(self, choices_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert the choices sheet to YAML format."""
        choices = []
        
        # Get reverse mappings for choices sheet
        sheets = Sheets()
        reverse_map = self.reverse_mappings.get(sheets.choices, {})
        
        for _, row in choices_df.iterrows():
            choice = {}
            
            for excel_col, value in row.items():
                if pd.isna(value) or value == '':
                    continue
                
                # Map Excel column to YAML field
                yaml_field = reverse_map.get(excel_col, excel_col.lower().replace(' ', '_'))
                choice[yaml_field] = str(value).strip()
            
            if choice:  # Only add non-empty choices
                choices.append(choice)
        
        return choices
    
    def _convert_settings_sheet(self, settings_df: pd.DataFrame) -> Dict[str, Any]:
        """Convert the settings sheet to YAML format."""
        settings = {}
        
        # Get reverse mappings for settings sheet
        sheets = Sheets()
        reverse_map = self.reverse_mappings.get(sheets.settings, {})
        
        # Settings are typically in key-value format
        for _, row in settings_df.iterrows():
            for excel_col, value in row.items():
                if pd.isna(value) or value == '':
                    continue
                
                # Map Excel column to YAML field
                yaml_field = reverse_map.get(excel_col, excel_col.lower().replace(' ', '_'))
                settings[yaml_field] = str(value).strip()
        
        return settings
    
    def _clean_type_value(self, type_value: str) -> str:
        """Clean and normalize question type values."""
        if not type_value:
            return 'text'
        
        # Remove extra whitespace and normalize
        cleaned = str(type_value).strip().lower()
        
        # Handle common variations
        type_mappings = {
            'begin group': 'group',
            'end group': 'end group',
            'begin repeat': 'repeat',
            'end repeat': 'end repeat',
            'select_one': 'select_one',
            'select_multiple': 'select_multiple',
            'select one': 'select_one',
            'select multiple': 'select_multiple',
        }
        
        return type_mappings.get(cleaned, cleaned)
    
    def _convert_yes_no_to_bool(self, value: str) -> bool:
        """Convert yes/no strings to boolean values."""
        if pd.isna(value):
            return False
        
        cleaned = str(value).strip().lower()
        return cleaned in ['yes', 'y', 'true', '1']
    
    def _process_groups_and_repeats(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process questions to properly nest groups and repeats."""
        processed = []
        stack = [processed]  # Stack to track current container
        
        for question in questions:
            q_type = question.get('type', '').lower()
            
            if q_type == 'group' or q_type == 'begin group':
                # Start a new group
                group = {
                    'type': 'group',
                    'name': question.get('name', ''),
                    'label': question.get('label', ''),
                    'children': []
                }
                
                # Copy other properties
                for key, value in question.items():
                    if key not in ['type', 'name', 'label']:
                        group[key] = value
                
                stack[-1].append(group)
                stack.append(group['children'])
                
            elif q_type == 'repeat' or q_type == 'begin repeat':
                # Start a new repeat
                repeat = {
                    'type': 'repeat',
                    'name': question.get('name', ''),
                    'label': question.get('label', ''),
                    'children': []
                }
                
                # Copy other properties
                for key, value in question.items():
                    if key not in ['type', 'name', 'label']:
                        repeat[key] = value
                
                stack[-1].append(repeat)
                stack.append(repeat['children'])
                
            elif q_type in ['end group', 'end repeat']:
                # End current group/repeat
                if len(stack) > 1:
                    stack.pop()
                else:
                    warnings.warn(f"Unmatched end statement: {q_type}")
                    
            else:
                # Regular question
                stack[-1].append(question)
        
        return processed
    
    def _save_yaml(self, data: Dict[str, Any], output_path: str):
        """Save YAML data to file with proper formatting."""
        # Use custom YAML dumper for better control
        class CustomDumper(yaml.SafeDumper):
            def increase_indent(self, flow=False, indentless=False):
                return super(CustomDumper, self).increase_indent(flow, False)
        
        # Custom YAML representer for better string formatting
        def str_presenter(dumper, data):
            if '\n' in data:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)
        
        CustomDumper.add_representer(str, str_presenter)
        
        # Ensure the output follows the correct structure:
        # settings:
        #   key: value
        # choices:
        #   - list_name: ...
        # survey:
        #   - type: ...
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, 
                     Dumper=CustomDumper,
                     default_flow_style=False,
                     allow_unicode=True,
                     sort_keys=False,
                     indent=2,
                     width=1000,  # Prevent line wrapping
                     explicit_start=False,
                     explicit_end=False)
    
    def validate_conversion(self, original_excel: str, converted_yaml: str) -> Dict[str, Any]:
        """
        Validate the conversion by converting back to Excel and comparing.
        
        Parameters
        ----------
        original_excel : str
            Path to original Excel file
        converted_yaml : str
            Path to converted YAML file
        
        Returns
        -------
        Dict[str, Any]
            Validation results with any differences found
        """
        # Convert YAML back to Excel
        form_data = FormData(self.version)
        form_data.load_yaml(converted_yaml)
        
        temp_excel = "temp_validation.xlsx"
        form_data.save_survey(temp_excel)
        
        try:
            # Compare the two Excel files
            original_data = pd.read_excel(original_excel, sheet_name=None, dtype=str)
            converted_data = pd.read_excel(temp_excel, sheet_name=None, dtype=str)
            
            validation_results = {
                'success': True,
                'differences': {},
                'warnings': []
            }
            
            # Compare each sheet
            for sheet_name in original_data.keys():
                if sheet_name not in converted_data:
                    validation_results['differences'][sheet_name] = "Sheet missing in converted file"
                    validation_results['success'] = False
                else:
                    # Compare DataFrames (basic comparison)
                    orig_df = original_data[sheet_name].fillna('')
                    conv_df = converted_data[sheet_name].fillna('')
                    
                    if not orig_df.equals(conv_df):
                        validation_results['differences'][sheet_name] = "Content differences detected"
                        validation_results['warnings'].append(
                            f"Sheet '{sheet_name}' has differences - this may be due to formatting or column ordering"
                        )
            
            return validation_results
            
        finally:
            # Clean up temp file
            if Path(temp_excel).exists():
                Path(temp_excel).unlink()


def convert_excel_to_yaml(excel_path: str, output_path: str, version: str = "3.22") -> Dict[str, Any]:
    """
    Convenience function to convert Excel to YAML.
    
    Parameters
    ----------
    excel_path : str
        Path to the Survey123 Excel file
    output_path : str
        Path to save the YAML file
    version : str, optional
        Survey123 version, by default "3.22"
    
    Returns
    -------
    Dict[str, Any]
        The converted survey data
    """
    converter = ExcelToYamlConverter(version)
    return converter.convert_excel_to_yaml(excel_path, output_path)