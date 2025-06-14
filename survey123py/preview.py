import re
import yaml

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
            
            if value or item.get("calculation"):

                ctx[item["name"]] = {"value": "", "type": item.get("type")}
                if item.get("type") == "integer":
                    value = int(value)
                elif item.get("type") == "decimal":
                    value = float(value)
                ctx[item["name"]]["value"] = value
                if item["type"] == "text":
                    # Need to escape quotes in the string so it can be used by eval() properly
                    ctx[item["name"]]["value"] = f"\"{ctx[item['name']]['value']}\""
            
            elif item["type"] == "group" or item["type"] == "repeat":

                for item2 in item["children"]:
                    value2 = item2.get("survey123py::preview_input")
                    if value2 or item2.get("calculation"):
                        ctx[item2["name"]] = {"value": "", "type": item2.get("type")}
                        if item2.get("type") == "integer":
                            value2 = int(value2)
                        elif item2.get("type") == "decimal":
                            value2 = float(value2)
                        ctx[item2["name"]]["value"] = value2
                        if item2["type"] == "text":
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
                    value = value.replace("${" + match + "}", ctx[match]["value"])
                ctx[item["name"]] = {"value": value, "type": item.get("type")}
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
            ctx[item["name"]]["value"] = eval(ctx[item["name"]]["value"])
            if ctx[item["name"]]["type"] == "text":
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
                if key not in ["type", "name", "label", "survey123py::preview_input", "children"]:

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
                    survey_data["survey"][i][key] = eval(value)

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
        