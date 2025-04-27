import re

class FormPreviewer:

    def __init__(self, yaml: str):
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
        # Load YAML file
        with open(yaml, 'r') as file:
            self.yaml_data = yaml.safe_load(file)
            # Create copy for output
            self.output_data = self.yaml_data.copy()
        self.ctx = self._load_ctx(self.yaml_data)

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
            if item.get("survey123py::preview_input"):
                ctx[item["name"]] = item.get("survey123py::preview_input")
            elif item["type"] == "group" or item["type"] == "repeat":
                for item2 in item["children"]:
                    if item2.get("survey123py::preview_input"):
                        ctx[item2["name"]] = item2.get("survey123py::preview_input")
        if len(ctx) == 0:
            raise ValueError("No preview input found in the YAML file. Please add survey123py::preview_input fields to the YAML file.")
        return ctx
    
    def _parse_vars(self, survey_data: dict):
        """
        This converts all variable references in the YAML data to their corresponding values in the data context
        (as  given by the `survey123py::preview_input field`).
        """
        # This pattern matches ${var_name} in the string
        pattern = r"\$\{(\w+)\}"

        for i, item in enumerate(survey_data["survey"]):
            if item["type"] == "group" or item["type"] == "repeat":
                for item2 in item["children"]:
                    if key not in ["type", "name"]:
                        for key, value in item2.items():
                            if isinstance(value, bool):
                                continue
                            matches = re.findall(pattern, value)
                            if matches:
                                # Replace ${} variable with variable in data ctx
                                survey_data["survey"][i]["children"][0][key] = item2[key].replace("${" + matches[0] + "}", self.ctx[matches[0]])
                continue
        for key, value in item.items():
            if key not in ["type", "name"]:
                matches = re.findall(pattern, value)
                if matches:
                    # Replace ${} variable with variable in data ctx
                    survey_data["survey"][i][key] = item[key].replace("${" + matches[0] + "}", self.ctx[matches[0]])
        return survey_data
    
    def _eval():
        """
        Placeholder for a safe eval() function.
        """
        raise NotImplementedError("This function is not implemented yet.")
        