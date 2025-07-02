import re
import yaml
from .formulas import *

class FormPreviewer:

    def __init__(self, yaml_path: str):
        """
        Test the output of a form by loading the YAML file and generating a preview of the form output.
        Note: this requires the yaml file to contain sample input using the column `survey123py::preview_input`
        such as below:

        ```
        survey:
            - type: text
              name: q1
              label: What is your favorite fruit?
              survey123py::preview_input: Apple
        ```

        Parameters
        ----------
        yaml : str
            Path to the YAML file containing survey data.
        """
        # This pattern matches ${var_name} in the string
        self.var_pattern = r"\$\{(\w+)\}"
        # Load YAML file
        with open(yaml_path, 'r') as file:
            self.yaml_data = yaml.safe_load(file)
            # Create copy for output
            self.output_data = self.yaml_data.copy()
        self.ctx = self._load_ctx()

    def _load_ctx(self) -> dict:
        """
        Load variables into data context as specified by survey123py::preview_input fields in the YAML file

        Parameters
        ----------
        yaml : str
            Path to the YAML file containing survey data.
        """
        ctx = {}
        for item in self.output_data["survey"]:
            value = item.get("survey123py::preview_input")
            
            if value is not None or item.get("calculation"):

                ctx[item["name"]] = {"value": "", "type": item.get("type")}
                if item.get("type") == "integer":
                    value = int(value)
                elif item.get("type") == "decimal":
                    value = float(value)
                ctx[item["name"]]["value"] = value
                if item["type"] == "text" and not isinstance(value, bool):
                    # Need to escape quotes in the string so it can be used by eval() properly
                    ctx[item["name"]]["value"] = f"\"{ctx[item['name']]['value']}\""
            
            elif item["type"] == "group" or item["type"] == "repeat":

                for item2 in item["children"]:
                    value2 = item2.get("survey123py::preview_input")
                    if value2 is not None or item2.get("calculation"):
                        ctx[item2["name"]] = {"value": "", "type": item2.get("type")}
                        if item2.get("type") == "integer":
                            value2 = int(value2)
                        elif item2.get("type") == "decimal":
                            value2 = float(value2)
                        ctx[item2["name"]]["value"] = value2
                        if item2["type"] == "text" and not isinstance(value2, bool):
                            # Need to escape quotes in the string so it can be used by eval() properly
                            ctx[item2["name"]]["value"] = f"\"{ctx[item2['name']]['value']}\""
        if len(ctx) == 0:
            raise ValueError("No preview input found in the YAML file. Please add survey123py::preview_input fields to the YAML file.")
        
        # Load calculation columns
        self.output_data["survey"]
        for item in [x for x in self.output_data["survey"] if "calculation" in x]:
            value = item["calculation"]
            matches = re.findall(self.var_pattern, value)
            if matches:
                for match in matches:
                    value = value.replace("${" + match + "}", str(ctx[match]["value"]))
                ctx[item["name"]] = {"value": value, "type": item.get("type")}
        
        # Load constraint columns (handle dot operator here)
        for item in [x for x in self.output_data["survey"] if "constraint" in x]:
            value = item["constraint"]
            
            # Handle dot operator - replace "." with current field's value
            if "." in value and "survey123py::preview_input" in item:
                current_field_value = item["survey123py::preview_input"]
                # Format the value appropriately for the constraint
                if item.get("type") == "text" and not isinstance(current_field_value, bool):
                    formatted_value = f'"{current_field_value}"'
                else:
                    formatted_value = str(current_field_value)
                
                # Replace standalone dots (not part of decimal numbers or method calls)
                # Use regex to match dots that are not between digits or after alphanumeric characters
                import re as regex_module
                value = regex_module.sub(r'(?<!\w)\.(?!\d)', formatted_value, value)
            
            # Handle variable substitutions in constraints
            matches = re.findall(self.var_pattern, value)
            if matches:
                for match in matches:
                    value = value.replace("${" + match + "}", str(ctx[match]["value"]))
            
            # Apply function name conversions for constraints
            if "if(" in value:
                value = value.replace("if(", "if_(")
            if "starts-with(" in value:
                value = value.replace("starts-with(", "starts_with(")
            if "int(" in value:
                value = value.replace("int(", "int_(")
            if "format-date(" in value:
                value = value.replace("format-date(", "format_date(")
            if "boolean-from-string(" in value:
                value = value.replace("boolean-from-string(", "boolean_from_string(")
            if "jr:choice-name(" in value:
                value = value.replace("jr:choice-name(", "jr_choice_name(")
            if "count-selected(" in value:
                value = value.replace("count-selected(", "count_selected(")
            if "decimal-date-time(" in value:
                value = value.replace("decimal-date-time(", "decimal_date_time(")
            if "date-time(" in value:
                value = value.replace("date-time(", "date_time(")
            if "not(" in value:
                value = value.replace("not(", "not_(")
            
            # Store constraint result in context for evaluation
            constraint_key = f"{item['name']}_constraint"
            ctx[constraint_key] = {"value": value, "type": "constraint"}
            
        # Check if calculation values need function name replacements
        for item in [x for x in self.output_data["survey"] if "calculation" in x]:
            if item["name"] in ctx:
                # Check if value to be evaluated contains things that need to be replaced
                if "if(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("if(", "if_(")
                if "starts-with(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("starts-with(", "starts_with(")
                if "int(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("int(", "int_(")
                if "format-date(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("format-date(", "format_date(")
                if "boolean-from-string(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("boolean-from-string(", "boolean_from_string(")
                if "jr:choice-name(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("jr:choice-name(", "jr_choice_name(")
                if "count-selected(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("count-selected(", "count_selected(")
                if "decimal-date-time(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("decimal-date-time(", "decimal_date_time(")
                if "date-time(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("date-time(", "date_time(")
                if "not(" in ctx[item["name"]]["value"]:
                    ctx[item["name"]]["value"] = ctx[item["name"]]["value"].replace("not(", "not_(")
                ctx[item["name"]]["value"] = eval(ctx[item["name"]]["value"])
            if ctx[item["name"]]["type"] == "text" and not isinstance(ctx[item["name"]]["value"], bool):
                # Need to escape quotes in the string so it can be used by eval() properly
                ctx[item["name"]]["value"] = f"\"{ctx[item['name']]['value']}\""

        return ctx
    
    def _parse_vars(self, survey_data: dict):
        """
        This converts all variable references in the YAML data to their corresponding values in the data context
        (as  given by the `survey123py::preview_input field`).
        """
        
        for i, item in enumerate(survey_data["survey"]):

            # Separate loop to handle nested children items (groups, repeaters)
            if item["type"] == "group" or item["type"] == "repeat":
                for item2 in item["children"]:
                    for key, value in item2.items():
                        if key not in ["type", "name", "survey123py::preview_input"]:
                            if isinstance(value, bool):
                                continue
                            matches = re.findall(self.var_pattern, value)
                            if matches:
                                for match in matches:
                                    if match in self.ctx:
                                        var_value = self.ctx[match]["value"]
                                        if key == "label" and isinstance(var_value, str):
                                            var_value = var_value[1:-1]  # Remove the quotes for necessary calculations. label does not support calculations
                                            
                                        out_value = item2[key].replace("${" + match + "}", str(var_value))
                                        
                                        # Replace ${} variable with variable in data ctx
                                        survey_data["survey"][i]["children"][0][key] = out_value
                                    else:
                                        var_name = "${" +  match + "}"
                                        raise ValueError(f"Element {var_name} not found in data context. Please check the YAML file.")
            
            for key, value in item.items():
                if key not in ["type", "name", "survey123py::preview_input", "children"]:
                    matches = re.findall(self.var_pattern, value)
                    if matches:
                        for match in matches:
                            if match in self.ctx:
                                var_value = self.ctx[match]["value"]
                                if key == "label" and isinstance(var_value, str):
                                    var_value = var_value[1:-1]  # Remove the quotes for necessary calculations. label does not support calculations

                                out_value = item[key].replace("${" + match + "}", str(var_value))

                                # Replace ${} variable with variable in data ctx
                                survey_data["survey"][i][key] = out_value
                            else:
                                var_name = "${" +  match + "}"
                                raise ValueError(f"Element {var_name} not found in data context. Please check the YAML file.")
        return survey_data
    
    def _parse_formulas(self, survey_data: dict):
        """
        Parses formulas in the YAML config. This must be used only after the variables have been parsed using
        `_parse_vars`
        """
        for i, item in enumerate(survey_data["survey"]):
            for key, value in item.items():
                if key not in ["type", "name", "label", "survey123py::preview_input", "children", "constraint"]:

                    # Note: This is called again (other one is in _load_ctx)
                    # This covers the survey data which is already parsed, for calculations it needs
                    # to be evaluated again for it to execute
                    if "if(" in value:
                        value = value.replace("if(", "if_(")
                    if "starts-with(" in value:
                        value = value.replace("starts-with(", "starts_with(")
                    if "int(" in value:
                        value = value.replace("int(", "int_(")
                    if "format-date(" in value:
                        value = value.replace("format-date(", "format_date(")
                    if "boolean-from-string(" in value:
                        value = value.replace("boolean-from-string(", "boolean_from_string(")
                    if "jr:choice-name(" in value:
                        value = value.replace("jr:choice-name(", "jr_choice_name(")
                    if "count-selected(" in value:
                        value = value.replace("count-selected(", "count_selected(")
                    if "decimal-date-time(" in value:
                        value = value.replace("decimal-date-time(", "decimal_date_time(")
                    if "date-time(" in value:
                        value = value.replace("date-time(", "date_time(")
                    if "not(" in value:
                        value = value.replace("not(", "not_(")
                    survey_data["survey"][i][key] = eval(value)

        return survey_data
    
    def _parse_constraints(self, survey_data: dict):
        """
        Parse constraint expressions and evaluate them, adding results to survey items.
        """
        for i, item in enumerate(survey_data["survey"]):
            if "name" in item:
                constraint_key = f"{item['name']}_constraint"
                if constraint_key in self.ctx and self.ctx[constraint_key]["type"] == "constraint":
                    value = self.ctx[constraint_key]["value"]
                    try:
                        # Evaluate the constraint expression
                        constraint_result = eval(value)
                        # Add constraint result to the survey item
                        survey_data["survey"][i]["constraint_result"] = constraint_result
                        survey_data["survey"][i]["constraint_expression"] = value
                    except Exception as e:
                        survey_data["survey"][i]["constraint_result"] = f"Error: {str(e)}"
                        survey_data["survey"][i]["constraint_expression"] = value
        
        return survey_data

    def show_preview(self, outpath: str = None):
        """
        Generate a preview of the form output by parsing the YAML file and replacing variable references with their values.

        Parameters
        ----------
        outpath : str, optional
            Path to save the preview output. If None, the output will not be saved to a file.
            Default is None.

        Returns
        -------
        dict
            The parsed survey data with variable references replaced by their values.
        """
        # Parse variables in the survey data
        self.output_data = self._parse_vars(self.output_data)
        self.output_data = self._parse_formulas(self.output_data)
        self.output_data = self._parse_constraints(self.output_data)

        if outpath:
            # Save the parsed survey data to a file if outpath is provided
            with open(outpath, 'w') as file:
                yaml.dump(self.output_data, file, default_flow_style=False)
        
        # Return the parsed survey data
        return self.output_data
    
    def _eval():
        """
        Placeholder for a safe eval() function.
        """
        raise NotImplementedError("This function is not implemented yet.")
        