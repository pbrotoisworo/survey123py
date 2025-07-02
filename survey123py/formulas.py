# All formulas available in Survey123 are implemented here.
# For full documentation, see: https://doc.arcgis.com/en/survey123/desktop/create-surveys/xlsformformulas.htm
from datetime import datetime
import math
import builtins

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

def atan(value: float) -> float:
    """
    Returns the arctangent of the value in radians.

    Example:

    `atan(${question_one})`
    """
    value = float(value)
    return math.atan(value)

def atan2(y: float, x: float) -> float:
    """
    Returns the arctangent of y/x in radians using the signs of both arguments
    to determine the quadrant of the result.

    Example:

    `atan2(${question_one}, ${question_two})`
    """
    y = float(y)
    x = float(x)
    return math.atan2(y, x)

def tan(value: float) -> float:
    """
    Returns the tangent of the value in radians.

    Example:

    `tan(${question_one})`
    """
    value = float(value)
    return math.tan(value)

def exp(value: float) -> float:
    """
    Returns e raised to the power of the value.

    Example:

    `exp(${question_one})`
    """
    value = float(value)
    return math.exp(value)

def exp10(value: float) -> float:
    """
    Returns 10 raised to the power of the value.

    Example:

    `exp10(${question_one})`
    """
    value = float(value)
    return math.pow(10, value)

def log(value: float) -> float:
    """
    Returns the natural logarithm of the value.
    Value must be positive.

    Example:

    `log(${question_one})`
    """
    value = float(value)
    if value <= 0:
        raise ValueError("Value must be positive")
    return math.log(value)

def log10(value: float) -> float:
    """
    Returns the base-10 logarithm of the value.
    Value must be positive.

    Example:

    `log10(${question_one})`
    """
    value = float(value)
    if value <= 0:
        raise ValueError("Value must be positive")
    return math.log10(value)

def pi() -> float:
    """
    Returns the mathematical constant π (pi).

    Example:

    `pi()`
    """
    return math.pi

def pow(base: float, exponent: float) -> float:
    """
    Returns base raised to the power of exponent.

    Example:

    `pow(${question_one}, ${question_two})`
    """
    base = float(base)
    exponent = float(exponent)
    return math.pow(base, exponent)

def round(value: float, ndigits: int = 0) -> float:
    """
    Returns the value rounded to the given number of digits after the decimal point.
    If ndigits is omitted or is None, it returns the nearest integer.

    Example:

    `round(${question_one}, 2)`
    """
    value = float(value)
    if ndigits == 0:
        return float(builtins.round(value))
    return builtins.round(value, ndigits)

def sqrt(value: float) -> float:
    """
    Returns the square root of the value.
    Value must be non-negative.

    Example:

    `sqrt(${question_one})`
    """
    value = float(value)
    if value < 0:
        raise ValueError("Value must be non-negative")
    return math.sqrt(value)

def selected(multi_select_answer: str, choice_value: str) -> bool:
    """
    Returns true if the choice_value is selected in the multi-select answer.
    The multi_select_answer should be a comma-separated string of selected values.

    Example:

    `selected(${multi_select_question}, 'option1')`
    """
    if not multi_select_answer or not choice_value:
        return False
    
    # Convert to string and split by commas to get individual selections
    selections = str(multi_select_answer).split(',')
    # Strip whitespace from each selection
    selections = [sel.strip() for sel in selections]
    return str(choice_value) in selections

def selected_at(multi_select_answer: str, index: int) -> str:
    """
    Returns the choice value at the specified index (0-based) in the multi-select answer.
    Returns empty string if index is out of bounds.
    The multi_select_answer should be a comma-separated string of selected values.

    Example:

    `selected-at(${multi_select_question}, 0)`
    """
    if not multi_select_answer:
        return ""
    
    # Convert to string and split by commas to get individual selections
    selections = str(multi_select_answer).split(',')
    # Strip whitespace from each selection
    selections = [sel.strip() for sel in selections]
    
    # Check if index is valid
    if index < 0 or index >= len(selections):
        return ""
    
    return selections[index]

def jr_choice_name(choice_value: str, question_name: str) -> str:
    """
    Returns the label/display text for a given choice value from a specified question.
    This is a simplified implementation that returns the choice_value since we don't have
    access to the choice definitions in the formula context.
    
    In a real Survey123 form, this would look up the label from the choices sheet
    based on the question's choice list.

    Example:

    `jr:choice-name(${priority}, 'priority')`
    """
    # In a real implementation, this would:
    # 1. Look up the question to find its choice list
    # 2. Look up the choice_value in that choice list
    # 3. Return the corresponding label
    # For now, we return the choice_value as a placeholder
    return str(choice_value) if choice_value else ""

def boolean(value: any) -> bool:
    """
    Converts the given value to a boolean.
    Returns true for non-zero numbers, non-empty strings, and boolean true.
    Returns false for zero, empty strings, None, and boolean false.

    Example:

    `boolean(${question_one})`
    """
    if value is None or value == "":
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.lower() not in ['', '0', 'false', 'no']
    return bool(value)

def coalesce(*args):
    """
    Returns the first non-null (non-empty) value from the arguments.
    
    Example:

    `coalesce(${optional_field}, ${backup_field}, 'default_value')`
    """
    for arg in args:
        if arg is not None and arg != "":
            return arg
    return ""

def count(*args):
    """
    Returns the count of non-null (non-empty) values from the arguments.
    
    Example:

    `count(${field1}, ${field2}, ${field3})`
    """
    count_val = 0
    for arg in args:
        if arg is not None and arg != "":
            count_val += 1
    return count_val

def count_selected(multi_select_answer: str) -> int:
    """
    Returns the number of selected choices in a multi-select answer.
    The multi_select_answer should be a comma-separated string of selected values.

    Example:

    `count-selected(${multi_select_question})`
    """
    if not multi_select_answer:
        return 0
    
    # Convert to string and split by commas to get individual selections
    selections = str(multi_select_answer).split(',')
    # Filter out empty selections after stripping whitespace
    selections = [sel.strip() for sel in selections if sel.strip()]
    return len(selections)

def date_time(value: str) -> str:
    """
    Converts a string to a Survey123 datetime object (unix timestamp in milliseconds).
    
    Example:

    `date-time(${datetime_question})`
    """
    if value is None or value == '':
        return None
    
    # Strip quotes if present
    if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    try:
        # Try parsing as ISO format first (YYYY-MM-DDTHH:MM:SS)
        if 'T' in value:
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        else:
            # Try parsing as date + time format
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return int(dt.timestamp() * 1000)
    except ValueError:
        try:
            # Fallback to date only
            dt = datetime.strptime(value, '%Y-%m-%d')
            return int(dt.timestamp() * 1000)
        except ValueError:
            raise ValueError(f"Value '{value}' is not a valid datetime format")

def decimal_date_time(timestamp) -> float:
    """
    Converts a timestamp (in milliseconds) to decimal date-time format.
    This represents the number of days since a reference date.
    
    Example:

    `decimal-date-time(${timestamp_field})`
    """
    if timestamp is None or timestamp == '':
        return None
    
    try:
        # Convert milliseconds to seconds and create datetime object
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        # Reference date (Excel epoch: January 1, 1900)
        # Note: Excel considers 1900 a leap year (it's not), so we use 1899-12-30
        reference_date = datetime(1899, 12, 30)
        delta = dt - reference_date
        return delta.total_seconds() / (24 * 60 * 60)  # Convert to days
    except (ValueError, TypeError):
        raise ValueError(f"Value '{timestamp}' is not a valid timestamp")

def false() -> bool:
    """
    Returns the boolean value false.
    
    Example:

    `false()`
    """
    return False

def join(separator: str, *args) -> str:
    """
    Joins multiple values with the specified separator.
    Only non-empty values are included in the result.
    
    Example:

    `join(' - ', ${field1}, ${field2}, ${field3})`
    """
    # Filter out None and empty string values
    valid_args = [str(arg) for arg in args if arg is not None and arg != ""]
    return str(separator).join(valid_args)

def max(*args):
    """
    Returns the maximum value from the arguments.
    Only considers numeric values.
    
    Example:

    `max(${field1}, ${field2}, ${field3})`
    """
    numeric_args = []
    for arg in args:
        if arg is not None and arg != "":
            try:
                numeric_args.append(float(arg))
            except (ValueError, TypeError):
                pass  # Skip non-numeric values
    
    if not numeric_args:
        return None
    
    return builtins.max(numeric_args)

def min(*args):
    """
    Returns the minimum value from the arguments.
    Only considers numeric values.
    
    Example:

    `min(${field1}, ${field2}, ${field3})`
    """
    numeric_args = []
    for arg in args:
        if arg is not None and arg != "":
            try:
                numeric_args.append(float(arg))
            except (ValueError, TypeError):
                pass  # Skip non-numeric values
    
    if not numeric_args:
        return None
    
    return builtins.min(numeric_args)

def not_(value) -> bool:
    """
    Returns the logical NOT of the value.
    Note: Function name uses underscore to avoid conflict with Python's 'not' keyword.
    
    Example:

    `not(${boolean_field})`
    """
    # Convert to boolean first, then negate
    return not boolean(value)

def now() -> int:
    """
    Returns the current date and time as a timestamp in milliseconds.
    
    Example:

    `now()`
    """
    return int(datetime.now().timestamp() * 1000)

def number(value) -> float:
    """
    Converts the value to a number (float).
    Returns None for values that cannot be converted.
    
    Example:

    `number(${text_field})`
    """
    if value is None or value == "":
        return None
    
    # Strip quotes if present
    if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None