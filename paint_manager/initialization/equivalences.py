"""Tableau d'équivalence tiré de https://www.1001hobbies.fr/content/28-tableau-d-equivalence-peinture.

https://www.planete-auto.fr/nuancier-et-tableau-equivalence-gunze-sangyo-mr-hobby/
https://www.nmc67.fr/phocadownload/Ressources/Documentations/Equivalence-peintures.pdf

"""

import itertools
import re
from collections import defaultdict
from typing import List

import requests

from paint_manager.initialization.npm67 import NMC67_DATA
from paint_manager.models import Paint, Reference, RegisteredSimilarPaint


class Mapper1001Hobbies:
    """Extract data from the 1001Hobbies website."""

    source_url = "https://www.1001hobbies.fr/content/28-tableau-d-equivalence-peinture"
    source_name = "1001Hobbies"

    def __init__(self):
        """Initialize the object."""
        self.existing_paints = defaultdict(lambda: defaultdict(lambda: []))
        for paint in Paint.objects.all().select_related("brand"):
            self.existing_paints[paint.brand.name][paint.reference].append(paint)

    def process(self, check=False):
        """Process the data to store them into the database."""
        print(f"Peintures similaires via {self.source_name}")
        source, __ = Reference.objects.get_or_create(name=self.source_name, defaults={"url": self.source_url})
        for line in self.load(check=check):
            if len(line) <= 1:
                continue
            if check:
                print(" /// ".join(str(x) for x in line))
            for equiv in itertools.combinations(line, 2):
                paint_a, paint_b = equiv
                if paint_a.id > paint_b.id:
                    paint_a, paint_b = paint_b, paint_a
                if not check:
                    RegisteredSimilarPaint.objects.get_or_create(source=source, paint_a=paint_a, paint_b=paint_b)

    def load(self, check=False) -> List[List[Paint]]:
        """Load the raw data and parse the table."""
        r = requests.get(self.source_url, timeout=60)
        text = r.text
        start = text.find("<strong>Fs#</strong></td>")
        start = text.find("<tr>", start)
        end = text.find("</tbody>", start)
        table_content = text[start:end]
        equivalences = []
        for row in table_content.split("</tr><tr>"):
            columns = re.findall(">(.*)</td>", row)
            equivalences.append(self.analyze_row(columns))
        return equivalences

    def analyze_row(self, values: List[str], check=False) -> List[Paint]:
        """Analyze a single row of the complete table."""
        paints = []
        for index, fn in [
            (3, self.get_tamiya),
            (5, self.get_revell),
            (9, self.get_gunze),
            (11, self.get_humbrol),
        ]:
            for sub_value in values[index].split("/"):
                paints += fn(sub_value.strip())
        paints = [x for x in paints if x]
        return paints

    def get_tamiya(self, text: str) -> List[Paint]:
        """Extract the Tamiya paints."""
        p = re.match(r"^(XF?)-?0?([1-9]\d*)$", text)
        if not p:
            return []
        finish, number = p.groups()
        text = f"{finish}-{number}"
        return self.existing_paints["Tamiya"][text]

    def get_revell(self, text: str) -> List[Paint]:
        """Extract the Revell paints."""
        if not re.match(r"^(\d+)$", text):
            return []
        text = "%02d" % int(text)
        return self.existing_paints["Revell Color"][text]

    def get_italeri(self, text: str) -> List[Paint]:
        """Extract the Italeri Acrylic Paint paints."""
        if not re.match(r"^4\d{3}AP$", text):
            return []
        return self.existing_paints["Italeri Acrylic Paint"][text]

    def get_humbrol(self, text: str) -> List[Paint]:
        """Extract the Humbrol paints."""
        if not re.match(r"^(\d+)$", text):
            return []
        text = "%03d" % int(text)
        return self.existing_paints["Humbrol"][text]

    def get_vallejo(self, text: str) -> List[Paint]:
        """Extract the Vallejo Model Color paints."""
        matcher = re.match(r"^(?:70\.)?(\d{3})$", text)
        if not matcher:
            return []
        text = "70.%03d" % int(matcher.group(1))
        return self.existing_paints["Vallejo Model Color"][text]

    def get_gunze(self, text: str) -> List[Paint]:
        """Extract the Gunze Sangyo paints."""
        matcher = re.match(r"^H?(\d+)$", text)
        if matcher:
            text = "H%d" % int(matcher.group(1))
            return self.existing_paints["Mr. Hobby - AQUEOUS HOBBY COLOR"][text]
        return []


class MapperPA(Mapper1001Hobbies):
    """Extract data from the planete-auto website."""

    source_url = "https://www.planete-auto.fr/nuancier-et-tableau-equivalence-gunze-sangyo-mr-hobby/"
    source_name = "planete-auto"

    def load(self, check=False) -> List[List[Paint]]:
        """Load the raw data and parse the table."""
        r = requests.get(self.source_url, timeout=60)
        text = r.text
        start = text.find("<tbody>")
        start = text.find("<tr", start)
        end = text.find("</tbody>", start)
        table_content = text[start:end]
        equivalences = []
        for row in table_content.split("</tr>"):
            columns = re.findall(">([^>]+)</td>", row)
            equivalences.append(self.analyze_row(columns, check=check))
        return equivalences

    def analyze_row(self, values: List[str], check=False) -> List[Paint]:
        """Analyze a single row of the complete table."""
        paints = []
        for index, fn in [
            (2, self.get_tamiya),
            (4, self.get_revell),
            (1, self.get_gunze),
            (3, self.get_humbrol),
        ]:
            if index >= len(values):
                continue
            for sub_value in values[index].split("/"):
                paints += fn(sub_value.strip())
        paints = [x for x in paints if x]
        return paints


class MapperNMC67(Mapper1001Hobbies):
    """Collect data from tne nmc67 website."""

    source_url = "https://www.nmc67.fr/phocadownload/Ressources/Documentations/Equivalence-peintures.pdf"
    source_name = "NMC67"

    def load(self, check=False):
        """Load all data."""
        equivalences = []
        for row in NMC67_DATA:
            row = row.replace(" /", "/")
            row = row.replace("/ ", "/")
            __, __, row = row.partition("Humbrol ")
            columns = row.split(" ")
            equivalences.append(self.analyze_row(columns, check=check))
        return equivalences

    def analyze_row(self, columns: List[str], check=False) -> List[Paint]:
        """Analyze a single row of the complete table."""
        paints = []
        for index, fn in [
            (0, self.get_humbrol),
            (1, self.get_tamiya),
            (2, self.get_revell),
            (4, self.get_gunze),
        ]:
            if index >= len(columns):
                continue
            for sub_value in columns[index].split("/"):
                paints += fn(sub_value.strip())
        paints = [x for x in paints if x]
        return paints


class MapperPhotoshopPlus(Mapper1001Hobbies):
    """Extract data from the Photoshop+ website."""

    source_url = "https://www.photoshoplus.fr/couleurs/correspondance-humbrol-autres/"
    source_name = "Photoshop+"

    def load(self, check=False) -> List[List[Paint]]:
        """Load the raw data and parse the table."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        }
        r = requests.get(self.source_url, headers=headers, timeout=60)
        text = r.text
        start = text.find('<table class="tablo2">')
        start = text.find("<tr", start)
        start = text.find("<tr", start + 1)
        end = text.find("</tbody>", start)
        table_content = text[start:end]
        equivalences = []
        for row in table_content.split("</tr>"):
            equivalences.append(self.analyze_row(row, check=check))
        return equivalences

    def analyze_row(self, row: str, check=False) -> List[Paint]:
        """Analyze a single row of the complete table."""
        row = row.replace("\n", "")
        if not row:
            return []
        matcher = re.match(r".*<strong>\s*(\d+)\s*&#8211;.*", row)
        paints = self.get_humbrol(matcher.group(1))
        for pattern, fn in [
            (
                r"<strong>Revell[^<]*</strong>[(\s]*([,\s\d]+)[)\s]*[<,]",
                self.get_revell,
            ),
            (
                r"<strong>Gunze Sangyo[^<]*</strong>[(\s]*([,\s\dH]+)[)\s]*[<,]",
                self.get_gunze,
            ),
            (
                r"<strong>Vallejo[^<]*</strong>[(\s]*([,\s\d]+)[)\s]*[<,]",
                self.get_vallejo,
            ),
            (
                r"<strong>Italeri[^<]*</strong>[(\s]*([,\s\dAP]+)[)\s]*[<,]",
                self.get_italeri,
            ),
            (
                r"<strong>Tamiya[^<]*</strong>[(\s]*([,\s\dXF\-]+)[)\s]*[<,]",
                self.get_tamiya,
            ),
        ]:
            for value in re.findall(pattern, row):
                for sub_value in value.split(","):
                    paints += fn(sub_value.strip())
        paints = [x for x in paints if x]
        return paints


def load_all_mappers():
    """Collect several equivalencies between paint brands."""
    m = MapperPA()
    m.process()
    # m = Mapper1001Hobbies()
    # m.process()
    m = MapperNMC67()
    m.process()
    # m = MapperPhotoshopPlus()
    # m.process()
