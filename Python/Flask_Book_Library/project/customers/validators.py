import re

# Letters (incl. Polish/Unicode), single spaces, hyphens, apostrophes and dots between words.
# No digits, no angle brackets, quotes, slashes etc. -> HTML/JS cannot be injected.
_TEXT_RE = re.compile(r"^[^\W\d_]+(?:[ '.\-][^\W\d_]+)*\.?$", re.UNICODE)

MAX_TEXT_LENGTH = 64   # matches the DB column size (String(64))
MIN_AGE = 0
MAX_AGE = 150


def validate_text(value, field):
    """Validate a name/city. Returns the stripped value or raises ValueError."""
    if not isinstance(value, str):
        raise ValueError(f'{field} must be a string')
    value = value.strip()
    if not value:
        raise ValueError(f'{field} must not be empty')
    if len(value) > MAX_TEXT_LENGTH:
        raise ValueError(f'{field} must be at most {MAX_TEXT_LENGTH} characters')
    if not _TEXT_RE.match(value):
        raise ValueError(f'{field} may contain only letters, spaces, hyphens, apostrophes and dots')
    return value


def validate_age(value):
    """Validate age. Returns an int or raises ValueError."""
    try:
        age = int(str(value).strip())
    except (ValueError, TypeError):
        raise ValueError('age must be an integer')
    if not MIN_AGE <= age <= MAX_AGE:
        raise ValueError(f'age must be between {MIN_AGE} and {MAX_AGE}')
    return age


def validate_customer(name, city, age):
    """Validate all customer fields. Returns (name, city, age) or raises ValueError."""
    return validate_text(name, 'name'), validate_text(city, 'city'), validate_age(age)
