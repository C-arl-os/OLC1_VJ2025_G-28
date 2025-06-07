from .Nodo import Expresion

class Multi(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda    
        self.derecha = derecha        

    def interpret(self):
        # Interpreta recursivamente ambos hijos y suma los resultados
        return self.izquierda.interpret() * self.derecha.interpret()

    def __str__(self):
        # Representación infija con paréntesis
        return f"({self.izquierda} * {self.derecha})"

    def __repr__(self):
        return f"Multiplicacion({self.izquierda!r}, {self.derecha!r})"
