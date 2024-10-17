from typing import Any
class Excepté(list):
    """
    Cette classe accepte zéro, un ou plusieurs éléments de type str
    et les stocke sous forme de liste.
    """
    def __init__(self, *liste_des_elements: str):
        """
        Initialise la liste avec les arguments passés qui doivent être de type str.
        :param args: Zéro, un ou plusieurs éléments de type str.
        """
        # On vérifie que tous les arguments sont des chaînes de caractères (str)
        if not all(isinstance(arg, str) for arg in liste_des_elements):
            raise ValueError("Tous les éléments doivent être de type 'str'.")

        # Initialisation de la liste avec les arguments donnés
        super().__init__(liste_des_elements)
def est_Excepté(instance:Any)->bool:
    return isinstance(instance,Excepté)
class Inclu(list):
    """
    Cette classe accepte zéro, un ou plusieurs éléments de type str
    et les stocke sous forme de liste.
    """
    def __init__(self, *liste_des_elements: str):
        """
        Initialise la liste avec les arguments passés qui doivent être de type str.
        :param args: Zéro, un ou plusieurs éléments de type str.
        """
        # On vérifie que tous les arguments sont des chaînes de caractères (str)
        if not all(isinstance(arg, str) for arg in liste_des_elements):
            raise ValueError("Tous les éléments doivent être de type 'str'.")

        # Initialisation de la liste avec les arguments donnés
        super().__init__(liste_des_elements)
def est_Inclu(instance:Any)->bool:
    return isinstance(instance,Inclu)
class Uniquement(list):
    """
    Cette classe accepte zéro, un ou plusieurs éléments de type str
    et les stocke sous forme de liste.
    """
    def __init__(self, *liste_des_elements: str):
        """
        Initialise la liste avec les arguments passés qui doivent être de type str.
        :param args: Zéro, un ou plusieurs éléments de type str.
        """
        # On vérifie que tous les arguments sont des chaînes de caractères (str)
        if not all(isinstance(arg, str) for arg in liste_des_elements):
            raise ValueError("Tous les éléments doivent être de type 'str'.")

        # Initialisation de la liste avec les arguments donnés
        super().__init__(liste_des_elements)
def est_Uniquement(instance:Any)->bool:
    return isinstance(instance, Inclu)


__all__ = [
    'Excepté',
    'est_Excepté',
    'Inclu',
    'est_Inclu',
    'Uniquement',
    'est_Uniquement'
]


def __dir__() -> list[str]:
    return __all__