import re

#Validator class provides functions to check if input is of correct format and length.

#Trims and enforces max length so that the input strings abide by the DB structure
def validate_string(value: str, max_length: int = None) -> None | bool | str:
    if value is None:
        return None

    try:
        value = str(value)
    except (TypeError, ValueError):
        print(f"Invalid string value: {value}")
        return False

    value = value.strip()

    if max_length and len(value) > max_length:
        return value[:max_length]
    return value

#Email format validation
def validate_email(email: str) -> None | bool | str:
    email = validate_string(email)

    if email in (None, False):
        return email

    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*$'
    if not re.match(pattern, email):
        print(f"Invalid email format: {email}")
        return False
    return email

#Convert to int or float then check bounds
def validate_number(value: int | float, num_type=int, minimum: int | float = None, maximum: int | float =None) ->(
        None | bool | int | float):
    if value is None:
        return None

    if num_type not in (int, float):
        print(f"Unsupported type {num_type}. Use int or float.")
        return False

    try:
        value = num_type(value)
    except (TypeError, ValueError):
        print(f"Invalid {num_type.__name__}: {value}")
        return False

    if minimum is not None and isinstance(minimum, (int,float)) and value < minimum:
        print(f"Value {value} is below minimum {minimum}.")
        return False
    if maximum is not None and isinstance(maximum, (int, float)) and value > maximum:
        print(f"Value {value} is above maximum {maximum}.")
        return False

    return value