# Survey123Py

[![Documentation Status](https://readthedocs.org/projects/survey123py/badge/?version=latest)](https://survey123py.readthedocs.io/en/latest/?badge=latest)

Survey123Py is a tool designed to simplify the creation of Survey123 forms by offering an alternative to the traditional Microsoft Excel workflow. Instead of managing complex forms in Excel with 40+ columns Survey123Py lets you define your form structure using YAML — making it easier to read, maintain, and track changes using version control systems like Git.

This package aims to enhance the developer experience by adding custom modules such as the `FormPreviewer` which allows you to verify output using samples inputs using the special field `survey123py::preview_input` in your YAML config.

In it's current form it is able to validate and parse formulas and variables the form. However, not all validation and parsing is included yet.

**Note**: Survey123Py does not publish your form. You’ll still need to use Survey123 Connect to publish the final version.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Survey123Py.

```bash
pip install git+https://github.com/pbrotoisworo/survey123py.git
```

## Usage

### Python
```python
from survey123py.form import FormData

survey = FormData(version="3.22")
survey.load_survey("Survey123FormConfig.yaml")
survey.save_survey("output.xlsx")
```

### CLI Usage

You can also use the CLI tool to generate Survey123 forms directly from the command line.

```bash
python main.py -v 3.22 --input sample_survey.yaml --output custom_output.xlsx
```

## YAML File
```yaml
settings:
  form_title: Asset Inspection
  instance_name: Asset_Inspection

choices:
  - list_name: yes_no
    name: yes
    label: Yes
  - list_name: yes_no
    name: no
    label: No
  - list_name: asset_types
    name: sign
    label: Sign
  - list_name: asset_types
    name: vehicle
    label: Vehicle

survey:
  - type: group
    name: groupInfo
    label: Asset Information
    children:
      - type: text
        name: assetCode
        label: Asset Code
        required: yes
      - type: select_one asset_types
        name: assetType
        label: What asset is this?
  - type: select_one yes_no
    name: assetStatus
    label: Asset passes inspection?
    hint: Answering "No" will require additional follow up inspection.
  - type: repeat
    name: repeat1
    label: Issue List
    children:
      - type: text
        name: issueDescription
        label: Add issue information if relevant
        readonly: yes
```

This results in the following outputs in Excel and Survey123 Connect
![YAML to Excel Output](survey123py/docs/img/readme_yaml_excel_output.png)
![YAML to Survey123 Output](survey123py/docs/img/readme_yaml_s123_output.png)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.