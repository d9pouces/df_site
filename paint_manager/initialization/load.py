"""After each migration, collect data from several websites."""

import re
from typing import Tuple

from paint_manager.initialization.encycolorpedia import (
    analyze_scalemates,
    scalemate,
)
from paint_manager.initialization.equivalences import load_all_mappers
from paint_manager.models import Brand, Paint
from paint_manager.utils import prepare_sorting_string

VALLEJO = "Vallejo Model Color"
REVELL = "Revell Color"
MR_HOBBY = "Mr. Hobby - Mr. COLOR"
MR_HOBBY_AQUEOUS = "Mr. Hobby - AQUEOUS HOBBY COLOR"
ITALERI = "Italeri Acrylic Paint"
ICM = "ICM"
TAMIYA = "Tamiya"
HUMBROL = "Humbrol"


# noinspection PyUnusedLocal
def database_initialization(sender, **kwargs):
    """Initialize all paint brands."""
    BrandAnalyzer(TAMIYA, "tamiya--655").analyze()
    BrandAnalyzer(HUMBROL, "humbrol--652").analyze()
    BrandAnalyzer(ICM, "icm--914").analyze()
    BrandAnalyzer(ITALERI, "italeri-acrylic-paint--678").analyze()
    BrandAnalyzer(MR_HOBBY_AQUEOUS, "mr-hobby--648").analyze()
    BrandAnalyzer(MR_HOBBY, "mr-hobby-mr-color--657").analyze()
    BrandAnalyzer(REVELL, "revell-color--653").analyze()
    BrandAnalyzer(VALLEJO, "vallejo-model-color--827").analyze()
    load_all_mappers()


class BrandAnalyzer:
    """Fetch all data about the given brand from the ScaleMates website."""

    def __init__(self, brand_name, brand_url):
        """Initialize the object."""
        self.brand_name = brand_name
        self.brand_url = brand_url

    def analyze(self):
        """Collect data from the ScaleMates website."""
        print(f"Récupération des peintures {self.brand_name}")
        brand, __ = Brand.objects.get_or_create(name=self.brand_name)
        for color in analyze_scalemates(self.brand_url):
            print(color)
            reference, name = self.get_name_reference(color)
            finish = self.get_finish(color)
            solvent = self.get_solvent(color)
            color_r = int(color.color[0:2], 16)
            color_g = int(color.color[2:4], 16)
            color_b = int(color.color[4:6], 16)
            size, packaging = self.get_packaging(color)
            if packaging not in {x[0] for x in Paint.PACKAGINGS}:
                print(["PACKAGINGS", color])
            if finish not in {x[0] for x in Paint.FINISHES}:
                print(["FINISHES", color])
            if solvent not in {x[0] for x in Paint.SOLVENTS}:
                print(["SOLVENTS", color])
            sort_name = prepare_sorting_string(name)
            sort_reference = prepare_sorting_string(reference)
            Paint.objects.get_or_create(
                reference=reference,
                finish=finish,
                sort_name=sort_name,
                sort_reference=sort_reference,
                solvent=solvent,
                size=size,
                brand=brand,
                packaging=packaging,
                color_r=color_r,
                color_g=color_g,
                color_b=color_b,
                defaults={"name": name},
            )

    @staticmethod
    def get_finish(color):
        """Return the finish from the raw string."""
        if not color.finish:
            return "unknown"
        return color.finish.lower()

    def get_name_reference(self, color) -> Tuple[str, str]:
        """Extract name and reference from the raw string."""
        reference = color.reference
        name = color.name
        if self.brand_name == TAMIYA:
            matcher = re.match(r"([A-Z]{1,2})-?(0\d+)", reference)
            if matcher:
                paint_type = matcher.group(1)
                paint_number = matcher.group(2)[1:]
                reference = f"{paint_type}-{paint_number}"
        return reference, name

    @staticmethod
    def get_solvent(color):
        """Extract the solvent from the raw string."""
        solvent = color.solvent.lower()
        if solvent == "acrylic lacquer":
            return "acrylic"
        elif color.reference.startswith("Tamiya 81"):
            return "acrylic"
        elif color.reference.startswith("Tamiya 80"):
            return "enamel"
        return solvent

    def get_packaging(self, color: scalemate) -> Tuple[str, str]:
        """Extract the packaging from the raw string."""
        matcher = re.match(r"(\d+ml) \((.+)\)", color.packaging)
        if matcher:
            if matcher.group(2) == "Spray can":
                packaging = "spray"
            elif matcher.group(2) == "Tinlet":
                packaging = "bottle"
            else:
                packaging = matcher.group(2).lower()
            size = matcher.group(1)
            return size, packaging
        matcher = re.match(r"((\d+)ml)", color.packaging)
        if matcher:
            if self.brand_name == "Tamiya" and color.name[:2] in {"AS-", "TS-", "PS-"}:
                packaging = "spray"
            elif self.brand_name in {
                TAMIYA,
                HUMBROL,
                ITALERI,
                MR_HOBBY_AQUEOUS,
                MR_HOBBY,
                VALLEJO,
            }:
                packaging = "bottle"
            elif self.brand_name == "Humbrol":
                packaging = "bottle"
            else:
                print(color)
                packaging = "bottle"
            size = matcher.group(1)
            return size, packaging
        matcher = re.match(r"(\d+) &amp; 05ml \(Tinlet\)", color.packaging)
        if matcher:
            size = matcher.group(1)
            return f"{size}ml", "bottle"
        print(color)
        return "", "bottle"
