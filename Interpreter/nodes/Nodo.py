class Expresion:
    """
    Clase base para los nodos del AST en el patrón Interpreter.
    Cada nodo debe implementar:
      - interpret() → devuelve el valor numérico de la subexpresión.
      - __str__()    → devuelve la representación infija de la subexpresión.
    """
    def interpret(self):
        raise NotImplementedError("interpret() no implementado en la subclase")

    def __str__(self):
        raise NotImplementedError("__str__() no implementado en la subclase")
