from .module import exporte, importe, Uniquement, Excepté, Inclu


def test(arg:str='ok') -> str:
    print(f'fonction test appele avec l argument {arg}')
    return f'fonction test renvoi la valeur {arg}'