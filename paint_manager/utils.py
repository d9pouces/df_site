"""Define some utility functions."""


def prepare_sorting_string(text: str) -> str:
    """Return a string easing the sort, adding leading zeros to any integer values.

    >>> prepare_sorting_string("X-11")
    'X-000011'

    """
    result = ""
    buffer = ""
    for c in text:
        if c in "0123456789":
            buffer += c
        else:
            if buffer:
                buffer_int = int(buffer)
                result += f"{buffer_int:06d}"
            buffer = ""
            result += c
    if buffer:
        buffer_int = int(buffer)
        result += f"{buffer_int:06d}"
    return result
