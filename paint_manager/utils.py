"""Define some utility functions."""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def preserve_request_query(request, url: str, query_arg: str = "_changelist_filters") -> str:
    """Preserve a query string in a URL."""
    current_value = request.GET.get(query_arg)
    if not current_value:
        return url
    parsed_url = list(urlparse(url))
    parsed_qs = dict(parse_qsl(parsed_url[4]))
    parsed_qs[query_arg] = current_value
    parsed_url[4] = urlencode(parsed_qs)
    return urlunparse(parsed_url)


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
