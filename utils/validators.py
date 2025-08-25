import re

#Validator class provides functions to check if input is of correct format and length.

#Trims and enforces max length so that the input strings abide by the DB structure
def validate_string(value: str, max_length: int = None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if max_length and len(value) > max_length:
        return value[:max_length]
    return value

#Email format validation
def validate_email(email: str) -> str | None:
    if email is None:
        return None
    email = email.strip()
    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*$'
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email}")
    return email

#Convert to int or float then check bounds
def validate_number(value, num_type=int, minimum=None, maximum=None):
    if value is None:
        return None

    if num_type not in (int, float):
        raise TypeError(f"Unsupported type {num_type}. Use int or float.")

    try:
        value = num_type(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid {num_type.__name__}: {value}")

    if minimum is not None and value < minimum:
        raise ValueError(f"Value {value} is below minimum {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"Value {value} is above maximum {maximum}.")

    return value