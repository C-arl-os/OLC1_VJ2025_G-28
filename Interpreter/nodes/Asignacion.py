from .Nodo import Expresion


class Asignacion(Expresion):
    def __init__(self, nombre_variable, valor):
        self.nombre_variable = nombre_variable  # Es un string (ID)
        self.valor = valor                      # Es una expresión (nodo del AST)

    def interpret(self):
        # Aquí solo devolvemos el valor interpretado. En un intérprete real, guardarías en un entorno.
        print(f"Asignando a '{self.nombre_variable}' el valor: {self.valor.interpret()}")
        return self.valor.interpret()

    def __str__(self):
        return f"{self.nombre_variable} = {self.valor}"

    def __repr__(self):
        return f"Asignacion('{self.nombre_variable}', {self.valor!r})"