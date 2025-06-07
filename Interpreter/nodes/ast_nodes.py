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


class Suma(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda    
        self.derecha = derecha        

    def interpret(self):
        # Interpreta recursivamente ambos hijos y suma los resultados
        return self.izquierda.interpret() + self.derecha.interpret()

    def __str__(self):
        # Representación infija con paréntesis
        return f"({self.izquierda} + {self.derecha})"

    def __repr__(self):
        return f"Suma({self.izquierda!r}, {self.derecha!r})"


class Resta(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        # Interpreta recursivamente ambos hijos y resta
        return self.izquierda.interpret() - self.derecha.interpret()

    def __str__(self):
        # Representación infija con paréntesis
        return f"({self.izquierda} - {self.derecha})"

    def __repr__(self):
        return f"Resta({self.izquierda!r}, {self.derecha!r})"

class Decimal(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def interpret(self):
        return self.valor

    def __str__(self):
        return str(self.valor)

    def __repr__(self):
        return f"Decimal({self.valor})"


class Caracter(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def interpret(self):
        return self.valor  

    def __str__(self):
        return f"'{self.valor}'"

    def __repr__(self):
        return f"Caracter('{self.valor}')"


class Cadena(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def interpret(self):
        return self.valor

    def __str__(self):
        return f'"{self.valor}"'

    def __repr__(self):
        return f"Cadena({self.valor!r})"


class Boleano(Expresion):
    def __init__(self, valor):
        self.valor = valor 

    def interpret(self):
        return self.valor

    def __str__(self):
        return "true" if self.valor else "false"

    def __repr__(self):
        return f"Boleano({self.valor})"


class Identificador(Expresion):
    def __init__(self, nombre):
        self.nombre = nombre

    def interpret(self):
      
        raise NotImplementedError("interpret() de Identificador necesita un contexto")

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Identificador('{self.nombre}')"


class Asignacion(Expresion):
    def __init__(self, tipo, identificador, valor):
        self.tipo = tipo          
        self.identificador = identificador  
        self.valor = valor        

    def interpret(self):
    
        return f"{self.tipo or ''} {self.identificador} = {self.valor.interpret()}"

    def __str__(self):
        return f"{self.tipo or ''} {self.identificador} = {self.valor};"

    def __repr__(self):
        return f"Asignacion(tipo={self.tipo!r}, identificador={self.identificador!r}, valor={self.valor!r})"