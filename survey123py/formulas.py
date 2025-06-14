# All formulas available in Survey123 are implemented here.
# For full documentation, see: https://doc.arcgis.com/en/survey123/desktop/create-surveys/xlsformformulas.htm
from datetime import datetime
import math

def if_(statement, a, b) -> bool:
    """
    If the conditstatemention evaluates to true, returns a; otherwise, returns b. For more information, see [Conditional expressions](https://doc.arcgis.com/en/survey123/desktop/create-surveys/xlsformexpressions.htm#ESRI_SECTION1_9C76E7A8118B493DB6A69AFA4AE37B9F).
    Note: String must be converted within survey123py from `if()` to `if_()` to avoid conflict with Python's built-in `if` statement.

    Example:

    if(selected(${question_one}, 'yes'), 'yes', 'no')
    """
    if isinstance(statement, str):
        if eval(statement):
            return a
        return b
    elif isinstance(statement, bool):
        if statement:
            return a
        return b
    else:
        raise ValueError(f"Value '{statement}' is unsupported. The statement must be a boolean or a string that can be evaluated to a boolean.")

def int_(value: str) -> int:
    """
    Converts the value to an integer. If this function is empty, it will return NaN and the question will remain empty.

    Example:

    `int(${question_one})`
    """
    if value is None or value == '':
        return None  # Return None for empty values to keep the question empty
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Value '{value}' is unsupported. The value must be a valid integer.")

def boolean_from_string(value: str) -> bool:
    """
    Returns true if the string provided is 'true' or '1'. Otherwise, returns false.

    Example:

    `boolean_from_string(${question_one})`
    """
    if value.lower() in ['true', '1']:
        return True
    elif value.lower() in ['false', '0']:
        return False
    else:
        raise ValueError(f"Value '{value}' is unsupported. The value must be 'true', 'false', '1', or '0'.")
    
def date(value: str) -> str:
    """
    Converts a number or string to a Survey123 date object (unix timestamp in milliseconds), without preserving time.

    Example:

    `date(${question_one})`
    """
    if value is None or value == '':
        return None  # Return None for empty values to keep the question empty
    try:
        outval = datetime.strptime(value, '%Y-%m-%d').timestamp() * 1000
        return int(outval)
    except ValueError:
        raise ValueError(f"Value '{value}' is unsupported. The value must be a valid date in 'YYYY-MM-DD' format.")

def format_date(datetime_val: str, format: str) -> str:
    """
    Fits an existing date or time value to a defined format. Input must be a date object.

    Example:

    `format_date(${question_one}, '%Y-%m-%d')`
    """
    # Convert milliseconds to seconds
    dt = datetime.fromtimestamp(datetime_val / 1000)
    # Format using the user-provided format string
    return dt.strftime(format)

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

    `starts_with(${question_one}, 'red')`
    """
    return string.startswith(substring)

def string_length(string: str) -> int:
    """
    Returns the length of the string.

    Example:

    `string_length(${question_one})`
    """
    return len(string)

def string(value: str) -> str:
    """
    Converts the value to a string.

    Example:

    `string(${question_one})`
    """
    return str(value)

def substr(string: str, start: int, end: int = None) -> str:
    """
    Returns a substring of the string starting at the specified index.
    If length is not specified, returns the substring from start to the end of the string.

    Example:

    `substr(${question_one}, 2, 5)`
    """
    if end is None:
        return string[start:]
    return string[start:start + end]

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

def cos(value: float) -> float:
    """
    Returns the cosine of the value in radians.

    Example:

    `cos(${question_one})`
    """
    value = float(value)
    return math.cos(value)

def sin(value: float) -> float:
    """
    Returns the sine of the value in radians.

    Example:

    `sin(${question_one})`
    """
    value = float(value)
    return math.sin(value)

def asin(value: float) -> float:
    """
    Returns the arcsine of the value in radians.
    Value must be in the range [-1, 1].

    Example:

    `asin(${question_one})`
    """
    value = float(value)
    if value < -1 or value > 1:
        raise ValueError("Value must be in the range [-1, 1]")
    return math.asin(value)