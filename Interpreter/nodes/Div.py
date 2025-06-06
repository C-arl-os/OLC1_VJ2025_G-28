from .Nodo import Expresion

class Div(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() / self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} / {self.derecha})"

    def __repr__(self):
        return f"Div({self.izquierda!r}, {self.derecha!r})"
