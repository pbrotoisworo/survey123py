# All formulas available in Survey123 are implemented here.
# For full documentation, see: https://doc.arcgis.com/en/survey123/desktop/create-surveys/xlsformformulas.htm
import math

def if_(statement, a, b) -> bool:
    """
    If the conditstatemention evaluates to true, returns a; otherwise, returns b. For more information, see [Conditional expressions](https://doc.arcgis.com/en/survey123/desktop/create-surveys/xlsformexpressions.htm#ESRI_SECTION1_9C76E7A8118B493DB6A69AFA4AE37B9F).
    Note: String must be converted within survey123py from `if()` to `if_()` to avoid conflict with Python's built-in `if` statement.

    Example:

    if(selected(${question_one}, 'yes'), 'yes', 'no')
    """
    if eval(statement):
        return a
    return b

def concat(*args):
    """
    Returns the concatenation of the string values.

    Example:

    `concat(${question_one}, ' and ', ${question_two})`
    """
    return ''.join(args)

def contains(string: str, substring: str):
    """
    Returns true if the given string contains the substring.

    Example:

    `contains(${question_one}, 'red')`
    """
    return substring in string

def starts_with(string: str, substring: str):
    """
    Returns true if the given string starts with the substring.

    Example:

    `starts-with(${question_one}, 'red')`
    """
    return string.startswith(substring)

def ends_with(string: str, substring: str):
    """
    Returns true if the given string ends with the substring.

    Example:

    `ends-with(${question_one}, 'hand.')z`
    """
    return string.endswith(substring)

def acos(value: float) -> float:
    """
    Returns the arccosine of the value in radians.
    Value must be in the range [-1, 1].

    Example:

    `acos(${question_one})`
    """
    value = float(value)
    if value < -1 or value > 1:
        raise ValueError("Value must be in the range [-1, 1]")
    return math.acos(value)