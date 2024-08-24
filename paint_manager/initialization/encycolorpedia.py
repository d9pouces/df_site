"""Module to search for colors in the encycolorpedia website."""

import re
from collections import namedtuple
from typing import Iterable, Optional

import requests


def search_color(pattern: str) -> Optional[str]:
    """Search for a pattern in the encycolorpedia website.

    >>> search_color("humbrol 240")  # Humbrol 240
    '96926d'
    >>> search_color("tamiya 80301") #  Tamiya XF1
    '333333'
    >>> search_color("tamiya 80025") #  Tamiya XF25
    '333333'

    :param pattern:
    :return:
    """
    r = requests.get("https://encycolorpedia.com/search", {"q": pattern}, timeout=60)
    if r.text.count("<h2>") != 1:
        return None
    matcher = re.match(r".*<article><h2><a href=/([\da-f]{6})>.*", r.text)
    if not matcher:
        return None

    return matcher.group(1)


scalemate = namedtuple("ScalemateColor", ["color", "name", "reference", "packaging", "finish", "solvent"])


def analyze_scalemates(brand: str) -> Iterable[scalemate]:
    """Analyze the scalemates website for a given brand to get all referenced paints.

    >>> list(analyze_scalemates("tamiya--655"))[0].name
    'X-5 Green'

    """
    r = requests.get(f"https://www.scalemates.com/colors/{brand}", timeout=60)
    content = r.text
    # with open("../../tamiya.html") as f:
    #     content = f.read()
    matcher = re.finditer(
        r'<div class="ac dg bgl cc pr mt4"><a href="[^"]+" class="al p8 c pf">'
        r'<div class="pr dib" style="width:180px;height:108px;background:#(?P<color>[\da-f]{6})">'
        r'<img src="/colors/img/logos/[^"]+" [^>]+></div></a>'
        r'<div class="ar"><a href="[^"]+" class=pf>'
        r'<span class="bgb nw">(?P<reference>[^<]+)</span> (?P<name>[^<]+)</a>'
        r"<div class=ut>[^<]+<br>(?P<packaging>[^<]+)</div>"
        r'(?:<div class="ccf c dib nw bgn">(?P<finish>[^<]+)</div>)'
        r"<div[^>]+>(?P<solvent>[^<]+)</div></div></div>",
        content,
        flags=re.DOTALL,
    )
    for match in matcher:
        yield scalemate(**match.groupdict())
