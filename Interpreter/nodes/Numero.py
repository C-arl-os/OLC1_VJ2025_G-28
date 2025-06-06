
from .Nodo import Expresion
    
class Numero(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def interpret(self):
        # Un número se interpreta a sí mismo
        return self.valor

    def __str__(self):
        # Para imprimir la expresión, basta con su propio valor
        return str(self.valor)

    def __repr__(self):
        return f"Numero({self.valor})"
