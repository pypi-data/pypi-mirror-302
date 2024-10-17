from types import ModuleType
from sys import modules
from inspect import getmembers
from .filtre import Uniquement,Excepté,Inclu
def _auto_all_and_dir_(module:ModuleType,*args:str|list[str]|Uniquement|Inclu|Excepté)->ModuleType:
    """
    Automatiser la gestion de __all__ et de __dir__.
    Il ajoute automatiquement tous les éléments publics du module dans __all__ et modifie __dir__ pour renvoyer __all__.
    """
    _Uniquement:list[str]=[]
    _on:bool=False
    _Inclu:list[str]=[]
    _Excepté:list[str]=[]

    for e in args:
        if isinstance(e,Uniquement):
            _Uniquement.extend(e)
            _on=True
        elif isinstance(e,Inclu):
            _Inclu.extend(e)
        elif isinstance(e,Excepté):
            _Excepté.extend(e)
        elif isinstance(e,list):
            _Uniquement.extend(e)
            _on=True
        elif isinstance(e,str):
            _Uniquement.extend(e)
            _on=True
    if _on==False:
        for name, _obj in getmembers(module):
        # Ajouter à __all__ seulement les objets publics (qui ne commencent pas par '_')
            if not name.startswith('_'):
                _Uniquement.extend(name)
                _on=True
    _Uniquement.extend(_Inclu)
    _Uniquement[:] = [item for item in _Uniquement if item not in _Excepté]
    _lst:list[str]=_Uniquement
    
    # Suppression des éléments présents dans _exclude de _Uniquement

    # Initialiser __all__ avec une liste vide si elle n'existe pas
    if not hasattr(module, '__all__'):
        module.__all__ = []

    # Parcourir les objets du module
    for name, _obj in getmembers(module):
        # Ajouter à __all__ seulement les objets publics (qui ne commencent pas par '_')
        if name in _lst:
            module.__all__.append(name)

    # Redéfinir __dir__ pour renvoyer __all__
    def __dir__()->list[str]:
        return module.__all__

    # Ajouter __dir__ au module
    module.__dir__ = __dir__

    return module

def exporte(module_name: str,*args:str|list[str]|Uniquement|Inclu|Excepté):
    """
    Vérifie si le module actuel doit appeler `auto_all_and_dir`.
    
    :param module_name: Le nom du module (généralement `__name__`).
    """
    if module_name == "__main__" or module_name == modules[module_name].__name__:
        _auto_all_and_dir_(modules[module_name],*args)


__all__ = [
    'exporte'
]


def __dir__() -> list[str]:
    return __all__