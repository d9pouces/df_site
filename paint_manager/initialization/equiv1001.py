"""Tableau d'équivalence tiré de https://www.1001hobbies.fr/content/28-tableau-d-equivalence-peinture .

Other references:
https://www.planete-auto.fr/nuancier-et-tableau-equivalence-gunze-sangyo-mr-hobby/
https://www.nmc67.fr/phocadownload/Ressources/Documentations/Equivalence-peintures.pdf.
"""

from df_config.manage import set_env

if __name__ == "__main__":
    set_env(module_name="paint_manager")
    import django

    django.setup()

    from paint_manager.initialization.equivalences import load_all_mappers

    load_all_mappers()
