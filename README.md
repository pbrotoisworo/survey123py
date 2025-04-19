# survey123py

Survey123py was built to provide an alternative to building a Survey123 Form using Microsoft Excel. By using YAML to build Survey123 forms it will allow for easier diff checking in version control systems and less overwhelm in checking an Excel sheet with 40+ columns.

Please take note this package does publish your Survey123 form. You have still have to do it via Survey123 Connect.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install survey123py.

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


### YAML File
```yaml
settings:
  form_title: Test Survey
  instance_name: Test_Instance
  namespaces: esri=https://esri.com/xforms

choices:
  - list_name: yes_no
    name: yes
    label: Yes
  - list_name: yes_no
    name: no
    label: No
  - list_name: yes_no_na
    name: yes
    label: Yes
  - list_name: yes_no_na
    name: no
    label: No
  - list_name: yes_no_na
    name: na
    label: NA

survey:
  - type: text
    name: q1
    label: What is your favorite fruit?
  - type: group
    name: group1
    label: Group 1
    children:
      - type: text
        name: q2
        label: What is your name?
        readonly: yes
      - type: integer
        name: q3
        label: What is your age?
        required: yes
  - type: group
    name: group2
    label: Group 2
    children:
      - type: text
        name: q4
        label: What is your favorite animal?
      - type: text
        name: q5
        label: What are your hobbies?
  - type: text
    name: q6
    label: What is your favorite color?
    hint: Please enter a color.
  - type: repeat
    name: repeat1
    label: Repeat Section
    children:
      - type: text
        name: q7
        label: What is your favorite book?
        readonly: yes
      - type: text
        name: q8
        label: What is your favorite movie?
        required: yes
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.