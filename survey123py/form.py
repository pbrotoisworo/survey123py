import json
from pathlib import Path
import shutil
import yaml
import pandas as pd
import openpyxl

class FormData:
    """
    Class to handle form data.
    """

    def __init__(self, version: str):
        self._module_dir = Path(__file__).parent
        self.sheets = {
            "survey": None,
            "choices": None,
            "settings": None,
            "Version": None,
            "Question types": None,
            "Appearances": None,
            "Field types": None,
            "Reference": None,
            "Reserved": None
        }
        self._template_paths = {
            "3.22": {
                "survey": self._module_dir / "template" / "template_3.22.xlsx",
                "columns": self._module_dir / "template" / "template_3.22_columns.json",
            },
        }
        self.yaml_data = None
        self.form_version = None
        self._load_template(version)
        

    def _load_template(self, version: str):
        """
        Load Survey123 template according to the version
        and store it in the sheets property to be filled in later.

        Parameters
        ----------
        version : str
            Template version being used for Survey123
        """

        
        if version not in self._template_paths.keys():
            raise ValueError(f"Version {version} not supported. Supported versions are: {list(self._template_paths.keys())}")

        for sheet_name in self.sheets.keys():
            try:
                self.sheets[sheet_name] = pd.read_excel(self._template_paths[version]["survey"], sheet_name=sheet_name)
            except ValueError as e:
                print(f"Error loading sheet {sheet_name}: {e}")
        self.form_version = self.sheets["Version"].iloc[1]["Unnamed: 1"]
    
    def load_survey(self, path: str):
        """
        Load YAML file containing survey data and convert it to a DataFrame.

        Parameters
        ----------
        path : str
            Path to the survey data file.
        """
        # Load YAML file
        with open(path, 'r') as file:
            survey_data = yaml.safe_load(file)
            self.yaml_data = survey_data

        with open(self._template_paths[self.form_version]["columns"]) as f:
            template_cols = json.load(f)

        for sheet_name in ["survey", "choices", "settings"]:
            if sheet_name not in survey_data.keys():
                print("WARNING: Sheet name not found in survey data:", sheet_name)
                continue

            if sheet_name == "settings":
                # Due to the way settings are structured, it is not in a list.
                # We need to convert it to a list so that it can be loaded into a DataFrame.
                if isinstance(survey_data[sheet_name], dict):
                    survey_data[sheet_name] = [survey_data[sheet_name]]
                self.sheets[sheet_name] = pd.DataFrame(survey_data[sheet_name])

            if sheet_name == "choices":
                choices_data_processed = []
                for field in survey_data[sheet_name]:
                    choices_data_processed.append(field)
                df_input = pd.DataFrame(choices_data_processed)
                df_input["name"] = df_input["name"].replace({True: "yes", False: "no"})
                df_input["label"] = df_input["label"].replace({True: "yes", False: "no"})
                df = pd.DataFrame(columns=template_cols[sheet_name])
                self.sheets[sheet_name] = pd.concat([df, df_input], axis=0, ignore_index=True)

            if sheet_name == "survey":
                survey_data_processed = []
                for _, field in enumerate(survey_data[sheet_name]):
                    
                    # Process groups and add the begin/end group statements automatically
                    if field["type"] == "group":
                        survey_data_processed.append({"type": "begin group", "name": field["name"], "label": field["label"]})
                        for child in field["children"]:
                            survey_data_processed.append(child)
                        survey_data_processed.append({"type": "end group"})
                        continue

                    # Process repeats and add the begin/end group statements automatically
                    if field["type"] == "repeat":
                        survey_data_processed.append({"type": "begin repeat", "name": field["name"], "label": field["label"]})
                        for child in field["children"]:
                            survey_data_processed.append(child)
                        survey_data_processed.append({"type": "end repeat"})
                        continue
                    survey_data_processed.append(field)
            
                df_input = pd.DataFrame(survey_data_processed)
                df_input["readonly"] = df_input["readonly"].map({True: "yes"})
                df_input["required"] = df_input["required"].map({True: "yes"})
                
                
                df = pd.DataFrame(columns=template_cols[sheet_name])
                self.sheets[sheet_name] = pd.concat([df, df_input], axis=0, ignore_index=True)

    def save_survey(self, outpath: str):
        """
        Save the survey data to the specified path.
        """
        # Copy template file to the output path and load it using openpyxl
        # to preserve formatting and styles
        shutil.copy(self._template_paths[self.form_version]["survey"], outpath)
        wb = openpyxl.load_workbook(outpath)

        with open(self._template_paths[self.form_version]["columns"]) as f:
            template_cols = json.load(f)
        
        # Iterate through the sheets and write the data to the corresponding sheets
        target_sheets = ["survey", "choices", "settings"]
        for sheet_name in list(self.yaml_data.keys()):
            sheet_data = self.sheets.get(sheet_name, None)
            if sheet_data is None or sheet_name not in target_sheets:
                continue
            
            print("Writing to sheet:", sheet_name)
            ws = wb[sheet_name]
            excel_col = None
            excel_row = None

            if sheet_name == "settings":
                input_data = sheet_data.iloc[0].to_dict()
                for col in template_cols["settings"]:
                    excel_col = template_cols["settings"][col]
                    excel_row = 2
                    target_cell = f"{excel_col}{excel_row}"
                    ws[target_cell].value = input_data.get(col, None)

            if sheet_name == "survey" or sheet_name == "choices":

                # Start at row 3 to give some space between column titles and data
                excel_row = 3

                for _, row in sheet_data.iterrows():
                    input_data = row.to_dict()
                    if sheet_name == "choices":
                        for col in template_cols["choices"]:
                            excel_col = template_cols["choices"][col]
                            target_cell = f"{excel_col}{excel_row}"
                            cell_data = input_data.get(col, None)
                            # if pd.isna(cell_data) is False:
                            #     print("Writing to cell", target_cell, ":", cell_data)
                            ws[target_cell].value = cell_data
                        excel_row += 1
                    
                    if sheet_name == "survey":
                        for col in template_cols["survey"]:
                            excel_col = template_cols["survey"][col]
                            target_cell = f"{excel_col}{excel_row}"
                            cell_data = input_data.get(col, None)
                            ws[target_cell].value = cell_data
                        excel_row += 1

        wb.save(outpath)

if __name__ == "__main__":
    pass
