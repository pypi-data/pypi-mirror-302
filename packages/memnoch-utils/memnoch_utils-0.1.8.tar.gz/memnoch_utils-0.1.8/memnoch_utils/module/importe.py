from typing import Optional
from types import ModuleType
import importlib.util
def importe(nom_du_module:str,chemin_du_fichier: str) -> Optional[ModuleType]:
    """
    Charge un module Python depuis un fichier spécifié et le retourne.

    :param chemin_du_fichier: Chemin absolu du fichier .py à charger.
    :return: Le module Python chargé, ou None en cas d'erreur.
    """
    try:
        # Crée une spécification pour le module
        spec = importlib.util.spec_from_file_location(nom_du_module, chemin_du_fichier,submodule_search_locations=[])
        if spec is None or spec.loader is None:
            return None  # Retourne None si la spécification n'a pas pu être créée

        # Crée le module à partir de la spécification
        mon_module = importlib.util.module_from_spec(spec)

        # Exécute le module dans son namespace
        spec.loader.exec_module(mon_module)

        # Retourne le module chargé
        return mon_module
    except Exception as e:
        print(f"Erreur lors du chargement du module : {e}")
        return None


__all__ = [
    'importe'
]


def __dir__() -> list[str]:
    return __all__