from contexto import tabla_variables
from .Nodo import Expresion
from contexto import tabla_variables, salidas_de_impresion
from tabla_simbolos.instancia import symbol_table as st
import math


class Numero(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def interpret(self):
        return self.valor

    def __str__(self):
        return str(self.valor)

    def __repr__(self):
        return f"Numero({self.valor})"
    
class Suma(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        tipo_izq = type(izq)
        tipo_der = type(der)

        # Clasificar los tipos
        def tipo(val):
            if isinstance(val, bool):
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        # Tabla de combinaciones válidas
        combinaciones_validas = {
            ("Entero", "Entero"): lambda a, b: a + b,
            ("Entero", "Decimal"): lambda a, b: a + b,
            ("Entero", "Carácter"): lambda a, b: a + ord(b),
            ("Entero", "Cadena"): lambda a, b: str(a) + b,

            ("Decimal", "Entero"): lambda a, b: a + b,
            ("Decimal", "Decimal"): lambda a, b: a + b,
            ("Decimal", "Carácter"): lambda a, b: a + ord(b),
            ("Decimal", "Cadena"): lambda a, b: str(a) + b,

            ("Carácter", "Entero"): lambda a, b: ord(a) + b,
            ("Carácter", "Decimal"): lambda a, b: ord(a) + b,
            ("Carácter", "Carácter"): lambda a, b: a + b,
            ("Carácter", "Cadena"): lambda a, b: a + b,

            ("Cadena", "Entero"): lambda a, b: a + str(b),
            ("Cadena", "Decimal"): lambda a, b: a + str(b),
            ("Cadena", "Booleano"): lambda a, b: a + str(b),
            ("Cadena", "Carácter"): lambda a, b: a + b,
            ("Cadena", "Cadena"): lambda a, b: a + b,

            ("Booleano", "Cadena"): lambda a, b: str(a) + b,
        }

        clave = (t_izq, t_der)
        if clave in combinaciones_validas:
            return combinaciones_validas[clave](izq, der)
        else:
            # Cambia este print por una excepción:
            raise Exception(f"Error: No se puede sumar tipos inválidos → {t_izq} + {t_der}")
    def __str__(self):
        return f"({self.izquierda} + {self.derecha})"

    def __repr__(self):
        return f"Suma({self.izquierda!r}, {self.derecha!r})"

class Resta(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        # Clasificar el tipo de cada operando (con detección de booleanos)
        def tipo(val):
            if isinstance(val, bool):
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        # Tabla de combinaciones válidas (basada en tu imagen)
        combinaciones_validas = {
            ("Entero", "Entero"): lambda a, b: a - b,
            ("Entero", "Decimal"): lambda a, b: a - b,
            ("Entero", "Carácter"): lambda a, b: a - ord(b),

            ("Decimal", "Entero"): lambda a, b: a - b,
            ("Decimal", "Decimal"): lambda a, b: a - b,
            ("Decimal", "Carácter"): lambda a, b: a - ord(b),

            ("Carácter", "Entero"): lambda a, b: ord(a) - b,
            ("Carácter", "Decimal"): lambda a, b: ord(a) - b,
        }

        clave = (t_izq, t_der)
        if clave in combinaciones_validas:
            return combinaciones_validas[clave](izq, der)
        else:
            
            print(f"Error: No se puede restar tipos inválidos → {t_izq} - {t_der}")
            raise Exception(f"Error: No se puede restar tipos inválidos → {t_izq} - {t_der}")
            #return None

    def __str__(self):
        return f"({self.izquierda} - {self.derecha})"

    def __repr__(self):
        return f"Resta({self.izquierda!r}, {self.derecha!r})"

class Multiplicacion(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        # Clasificar tipo
        def tipo(val):
            if isinstance(val, bool):
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        # Tabla de combinaciones válidas
        combinaciones_validas = {
            ("Entero", "Entero"): lambda a, b: a * b,
            ("Entero", "Decimal"): lambda a, b: a * b,
            ("Entero", "Carácter"): lambda a, b: a * ord(b),

            ("Decimal", "Entero"): lambda a, b: a * b,
            ("Decimal", "Decimal"): lambda a, b: a * b,
            ("Decimal", "Carácter"): lambda a, b: a * ord(b),

            ("Carácter", "Entero"): lambda a, b: ord(a) * b,
            ("Carácter", "Decimal"): lambda a, b: ord(a) * b,
        }

        clave = (t_izq, t_der)
        if clave in combinaciones_validas:
            return combinaciones_validas[clave](izq, der)
        else:
            print(f"Error: No se puede multiplicar tipos inválidos → {t_izq} * {t_der}")
            raise Exception(f"Error: No se puede multiplicar tipos inválidos → {t_izq} * {t_der}")

            #return None

    def __str__(self):
        return f"({self.izquierda} * {self.derecha})"

    def __repr__(self):
        return f"Multiplicacion({self.izquierda!r}, {self.derecha!r})"

class Division(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        # Clasificación de tipo
        def tipo(val):
            if isinstance(val, bool):
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        # Validar combinación
        combinaciones_validas = {
            ("Entero", "Entero"): lambda a, b: float(a) / b,
            ("Entero", "Decimal"): lambda a, b: float(a) / b,
            ("Entero", "Carácter"): lambda a, b: float(a) / ord(b),

            ("Decimal", "Entero"): lambda a, b: a / b,
            ("Decimal", "Decimal"): lambda a, b: a / b,
            ("Decimal", "Carácter"): lambda a, b: a / ord(b),

            ("Carácter", "Entero"): lambda a, b: float(ord(a)) / b,
            ("Carácter", "Decimal"): lambda a, b: float(ord(a)) / b,
        }

        clave = (t_izq, t_der)

        try:
            if clave in combinaciones_validas:
                return combinaciones_validas[clave](izq, der)
            else:
                print(f"Error: No se puede dividir tipos inválidos → {t_izq} / {t_der}")
                raise Exception(f"Error: No se puede dividir tipos inválidos → {t_izq} / {t_der}")
                #return None
        except ZeroDivisionError:
            print("Error: División por cero.")
            raise Exception(f"Error: División por cero")
            #return None

    def __str__(self):
        return f"({self.izquierda} / {self.derecha})"

    def __repr__(self):
        return f"Division({self.izquierda!r}, {self.derecha!r})"

class Potencia(Expresion):
    def __init__(self, base, exponente):
        self.base = base
        self.exponente = exponente

    def interpret(self):
        base_val = self.base.interpret()
        exponente_val = self.exponente.interpret()

        # Clasificación de tipos
        def tipo(val):
            if isinstance(val, bool):
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_base = tipo(base_val)
        t_exponente = tipo(exponente_val)

        # Combinaciones válidas
        combinaciones_validas = {
            ("Entero", "Entero"): lambda a, b: a ** b,
            ("Entero", "Decimal"): lambda a, b: a ** b,
            ("Decimal", "Entero"): lambda a, b: a ** b,
            ("Decimal", "Decimal"): lambda a, b: a ** b,
        }

        clave = (t_base, t_exponente)
        if clave in combinaciones_validas:
            resultado = combinaciones_validas[clave](base_val, exponente_val)
            # Retornar según el tipo dominante
            if isinstance(base_val, float) or isinstance(exponente_val, float):
                return float(resultado)
            else:
                return int(resultado)
        else:            
            print(f"Error: No se puede aplicar potencia a tipos inválidos → {t_base} ** {t_exponente}")
            raise Exception(f"Error: No se puede aplicar potencia a tipos inválidos → {t_base} ** {t_exponente}")
            #return None

    def __str__(self):
        return f"({self.base} ** {self.exponente})"

    def __repr__(self):
        return f"Potencia({self.base!r}, {self.exponente!r})"

class Seno(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        valor = self.expresion.interpret()
        # Solo acepta int o float
        if not isinstance(valor, (int, float)):
            raise Exception(f"Error: El argumento de seno debe ser un número, se recibió {type(valor).__name__}")
        return math.sin(valor)

    def __str__(self):
        return f"sin({self.expresion})"

    def __repr__(self):
        return f"Seno({self.expresion!r})"

class Coseno(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        valor = self.expresion.interpret()
        # Solo acepta int o float
        if not isinstance(valor, (int, float)):
            raise Exception(f"Error: El argumento de coseno debe ser un número, se recibió {type(valor).__name__}")
        return math.cos(valor)

    def __str__(self):
        return f"cos({self.expresion})"

    def __repr__(self):
        return f"Coseno({self.expresion!r})"

class Inversa(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        valor = self.expresion.interpret()
        if not isinstance(valor, int):
            raise Exception(f"Error: El argumento de Inv debe ser un entero, se recibió {type(valor).__name__}")
        # Reordena los dígitos (invierte el número)
        signo = -1 if valor < 0 else 1
        valor_abs = abs(valor)
        invertido = int(str(valor_abs)[::-1])
        return signo * invertido

    def __str__(self):
        return f"Inv({self.expresion})"

    def __repr__(self):
        return f"Inversa({self.expresion!r})"

class Modulo(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq_val = self.izquierda.interpret()
        der_val = self.derecha.interpret()

        # Clasificar tipo
        def tipo(val):
            if isinstance(val, bool):  # Excluir explícitamente booleanos
                return "Booleano"
            elif isinstance(val, int):
                return "Entero"
            elif isinstance(val, float):
                return "Decimal"
            elif isinstance(val, str):
                return "Cadena" if len(val) > 1 else "Carácter"
            else:
                return "Desconocido"

        t_izq = tipo(izq_val)
        t_der = tipo(der_val)

        # Combinaciones válidas
        combinaciones_validas = {
            ("Entero", "Entero"),
            ("Entero", "Decimal"),
            ("Decimal", "Entero"),
            ("Decimal", "Decimal"),
        }

        if (t_izq, t_der) not in combinaciones_validas:
            print(f"Error: No se puede aplicar módulo a tipos → {t_izq} % {t_der}")
            raise Exception(f"Error: No se puede aplicar módulo a tipos → {t_izq} % {t_der}")
            #return None

        try:
            resultado = izq_val % der_val
            return float(resultado)  # Siempre devuelve decimal
        except ZeroDivisionError:
            print("Error: módulo por cero.")
            raise Exception(f"Error: División por cero")
            #return None

    def __str__(self):
        return f"({self.izquierda} % {self.derecha})"

    def __repr__(self):
        return f"Modulo({self.izquierda!r}, {self.derecha!r})"

class Negativo(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        valor = self.expresion.interpret()
        # Verifica tipo
        if isinstance(valor, bool):
            tipo = "Booleano"
        elif isinstance(valor, int):
            tipo = "Entero"
        elif isinstance(valor, float):
            tipo = "Decimal"
        elif isinstance(valor, str):
            if len(valor) == 1:
                tipo = "Caracter"
            else: 
                tipo = "Cadena"
        else:
            tipo = "Desconocido"

        if tipo not in ("Entero", "Decimal"):
            print(f"Error: No se puede aplicar negación a tipo {tipo}")
            raise Exception(f"Error: No se puede aplicar negación a tipo {tipo}")

        return -valor

    def __str__(self):
        return f"-({self.expresion})"

    def __repr__(self):
        return f"Negativo({self.expresion!r})"

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
        # Si el valor ya es un solo carácter, conviértelo a su código ASCII
        # if isinstance(valor, str) and len(valor) == 1:
        #     self.valor = ord(valor)
        # else:
        #     # Si por alguna razón no es un carácter válido, puedes manejarlo aquí
        #     self.valor = valor

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

'''class Boleano(Expresion):
    def __init__(self, valor):  # valor puede ser 'true' o 'false' como string
        self.valor = valor  # por si lo escribes en mayúsculas

    def interpret(self):
        return True if self.valor == 'true' else False

    def __str__(self):
        return "true" if self.valor == 'true' else "false"

    def __repr__(self):
        return f"Boleano({self.valor})"'''

class Identificador(Expresion):
    def __init__(self, nombre):
        self.nombre = nombre

    def interpret(self):
        if self.nombre in tabla_variables:
            return tabla_variables[self.nombre]
        else:
            raise Exception(f"Variable '{self.nombre}' no ha sido definida")

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Identificador('{self.nombre}')"

class Declaracion(Expresion):
    def __init__(self, tipo, identificador, linea=None, columna=None):
        self.tipo = tipo
        self.identificador = identificador
        self.linea = linea
        self.columna = columna


    def interpret(self):
        # Verificar si la variable ya está declarada
        if self.identificador in tabla_variables:
            raise Exception(f"Error semántico: '{self.identificador}' ya ha sido declarado.")

        # Si no existe, declararla con un valor por defecto
        if self.tipo == "int":
            tabla_variables[self.identificador] = 0
        elif self.tipo == "float":
            tabla_variables[self.identificador] = 0.0
        elif self.tipo == "char":
            tabla_variables[self.identificador] = '\0'
        elif self.tipo == "string":
            tabla_variables[self.identificador] = ""
        elif self.tipo == "bool":
            tabla_variables[self.identificador] = False
        else:
            tabla_variables[self.identificador] = None

        return f"{self.tipo} {self.identificador} declarado."


    def __str__(self):
        return f"{self.tipo} {self.identificador};"

    def __repr__(self):
        return f"Declaracion(tipo={self.tipo!r}, identificador={self.identificador!r})"

class Asignacion(Expresion):
    def __init__(self, tipo, identificador, valor): # Este es el __init__ correcto para Asignacion
        self.tipo = tipo
        self.identificador = identificador
        self.valor = valor

    def interpret(self):
        valor_interpretado = self.valor.interpret()
        tabla_variables[self.identificador] = valor_interpretado
        return valor_interpretado

    def __str__(self):
        return f"{self.tipo} {self.identificador} = {self.valor}"

    def __repr__(self):
        return f"Asignacion(tipo={self.tipo!r}, identificador={self.identificador!r}, valor={self.valor!r})"

class Println(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        valor_a_imprimir = None
        if isinstance(self.expresion, Identificador):
            nombre = self.expresion.nombre
            if nombre in tabla_variables:
                valor_a_imprimir = tabla_variables[nombre]
            else:
                raise Exception(f"Variable '{nombre}' no ha sido definida")
        else:
            valor_a_imprimir = self.expresion.interpret()
        
        salidas_de_impresion.append(str(valor_a_imprimir))
        return valor_a_imprimir 

    def __str__(self):
        return f"Println({self.expresion})"

    def __repr__(self):
        return f"Println({self.expresion!r})"
    
class ErrorPrintln(Expresion):
    def __init__(self, contenido, mensaje, linea=None, columna=None):
        self.contenido = contenido
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def interpret(self):
        raise Exception(
            f"Error en println: {self.mensaje} -> '{self.contenido}'"
        )

    def __str__(self):
        return f"ErrorPrintln({self.mensaje}: {self.contenido})"

    def __repr__(self):
        return str(self)

#operadores

class Relacional(Expresion):
    def __init__(self, izquierda, derecha, operador):
        self.izquierda = izquierda
        self.derecha = derecha
        self.operador = operador

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        def tipo(val):
            if type(val) is bool:
                return "Booleano"
            elif type(val) is int:
                return "Entero"
            elif type(val) is float:
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        # Tabla de combinaciones válidas
        combinaciones_validas = {
            ("Entero", "Entero"), ("Entero", "Decimal"), ("Entero", "Carácter"),
            ("Decimal", "Entero"), ("Decimal", "Decimal"), ("Decimal", "Carácter"),
            ("Carácter", "Entero"), ("Carácter", "Decimal"), ("Carácter", "Carácter"),
            ("Booleano", "Booleano"),
            ("Cadena", "Cadena")
        }

        if (t_izq, t_der) not in combinaciones_validas:
            print(f"Error: Comparación no válida entre tipos → {t_izq} {self.operador} {t_der}")
            raise Exception(f"Error: Comparación no válida entre tipos → {t_izq} {self.operador} {t_der}")
            #return None

        try:
            if self.operador == ">":
                return izq > der
            elif self.operador == "<":
                return izq < der
            elif self.operador == ">=":
                return izq >= der
            elif self.operador == "<=":
                return izq <= der
            elif self.operador == "==":
                return izq == der
        except Exception as e:
            print(f"Error al comparar: {e}")
            return None

    def __str__(self):
        return f"({self.izquierda} {self.operador} {self.derecha})"

class MayorQue(Relacional):
    def __init__(self, izquierda, derecha):
        super().__init__(izquierda, derecha, ">")

class MenorQue(Relacional):
    def __init__(self, izquierda, derecha):
        super().__init__(izquierda, derecha, "<")

class MayorIgual(Relacional):
    def __init__(self, izquierda, derecha):
        super().__init__(izquierda, derecha, ">=")

class MenorIgual(Relacional):
    def __init__(self, izquierda, derecha):
        super().__init__(izquierda, derecha, "<=")

class Igual(Relacional):
    def __init__(self, izquierda, derecha):
        super().__init__(izquierda, derecha, "==")

# ...DECREMENTO Y iNCREMENTO...

class Incremento(Expresion):
    def __init__(self, identificador):
        self.identificador = identificador

    def interpret(self):
        if self.identificador.nombre in tabla_variables:
            tabla_variables[self.identificador.nombre] += 1
            return tabla_variables[self.identificador.nombre]
        else:
            raise Exception(f"Variable '{self.identificador.nombre}' no ha sido definida")

    def __str__(self):
        return f"{self.identificador}++"

    def __repr__(self):
        return f"Incremento({self.identificador!r})"

class Decremento(Expresion):
    def __init__(self, identificador):
        self.identificador = identificador

    def interpret(self):
        if self.identificador.nombre in tabla_variables:
            tabla_variables[self.identificador.nombre] -= 1
            return tabla_variables[self.identificador.nombre]
        else:
            raise Exception(f"Variable '{self.identificador.nombre}' no ha sido definida")

    def __str__(self):
        return f"{self.identificador}--"

    def __repr__(self):
        return f"Decremento({self.identificador!r})"
    
class OrLogicoNode:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        def tipo(val):
            if type(val) is bool:
                return "Booleano"
            elif type(val) is int:
                return "Entero"
            elif type(val) is float:
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                else:
                    return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        if t_izq != "Booleano" or t_der != "Booleano":
            print(f"Error: Operación lógica '||' solo válida entre booleanos → {t_izq} || {t_der}")
            raise Exception(f"Error: Operación lógica '||' solo válida entre booleanos → {t_izq} || {t_der}")

        return izq or der

    def __repr__(self):
        return f'({self.izquierda} || {self.derecha})'

class AndLogicoNode:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        def tipo(val):
            if type(val) is bool:
                return "Booleano"
            elif type(val) is int:
                return "Entero"
            elif type(val) is float:
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                else:
                    return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        if t_izq != "Booleano" or t_der != "Booleano":
            print(f"Error: Operación lógica '&&' solo válida entre booleanos → {t_izq} && {t_der}")
            raise Exception(f"Error: Operación lógica '&&' solo válida entre booleanos → {t_izq} && {t_der}")

        return izq and der

    def __str__(self):
        return f"({self.izquierda} && {self.derecha})"

class NotLogicoNode:
    def __init__(self, expr):
        self.expr = expr

    def interpret(self):
        val = self.expr.interpret()

        def tipo(val):
            if type(val) is bool:
                return "Booleano"
            elif type(val) is int:
                return "Entero"
            elif type(val) is float:
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                else:
                    return "Cadena"
            return "Desconocido"

        t_val = tipo(val)

        if t_val != "Booleano":
            print(f"Error: Operación lógica '!' solo válida sobre booleano → !{t_val}")
            raise Exception(f"Error: Operación lógica '!' solo válida sobre booleano → !{t_val}")

        return not val

    def __str__(self):
        return f"(!{self.expr})"

class XorLogicoNode:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq = self.izquierda.interpret()
        der = self.derecha.interpret()

        def tipo(val):
            if type(val) is bool:
                return "Booleano"
            elif type(val) is int:
                return "Entero"
            elif type(val) is float:
                return "Decimal"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "Carácter"
                else:
                    return "Cadena"
            return "Desconocido"

        t_izq = tipo(izq)
        t_der = tipo(der)

        if t_izq != "Booleano" or t_der != "Booleano":
            print(f"Error: Operación lógica '^' solo válida entre booleanos → {t_izq} ^ {t_der}")
            raise Exception(f"Error: Operación lógica '^' solo válida entre booleanos → {t_izq} ^ {t_der}")

        return izq ^ der

    def __str__(self):
        return f"({self.izquierda} ^ {self.derecha})"

#Ciclo while 

class Instruccion(Expresion):
    def __init__(self, instruccion):
        self.instruccion = instruccion

    def interpret(self):
        return self.instruccion.interpret()
    
    def __str__(self):
        print(self.instruccion)
        return f""
    
    
class Instrucciones(Expresion):
    def __init__(self, instruccion, instrucciones=None):
        if instrucciones is not None:
            self.instrucciones = instrucciones.instrucciones.copy()
        else:
            self.instrucciones = []
        self.instrucciones.append(instruccion)

    def interpret(self, errores_semanticos=None):
        results = []
        if errores_semanticos is None:
            errores_semanticos = []
        for instr in self.instrucciones:
            try:
                # Si el nodo tiene interpret con errores_semanticos, pásalo
                if hasattr(instr, 'interpret') and instr.interpret.__code__.co_argcount == 2:
                    results.append(instr.interpret(errores_semanticos))
                else:
                    results.append(instr.interpret())
            except Exception as e:
                errores_semanticos.append({
                    'tipo': 'Semántico',
                    'descripcion': str(e),
                    'linea': getattr(instr, 'linea', -1),
                    'columna': getattr(instr, 'columna', -1)
                })
        return results

    def __str__(self):
        return "\n".join(str(instr) for instr in self.instrucciones)
  
class Instrucciones(Expresion):
    def __init__(self, instruccion, instrucciones=None):
        if instrucciones is not None:
            self.instrucciones = instrucciones.instrucciones.copy()
        else:
            self.instrucciones = []
        self.instrucciones.append(instruccion)

    def interpret(self, errores_semanticos=None):
        if errores_semanticos is None:
            errores_semanticos = []
        for instr in self.instrucciones:
            try:
                if hasattr(instr, 'interpret') and instr.interpret.__code__.co_argcount == 2:
                    res = instr.interpret(errores_semanticos)
                else:
                    res = instr.interpret()
                # Si la instrucción es Break o Continue, propágalo inmediatamente
                if isinstance(res, Break) or isinstance(res, Continue):
                    return res
            except Exception as e:
                errores_semanticos.append({
                    'tipo': 'Semántico',
                    'descripcion': str(e),
                    'linea': getattr(instr, 'linea', -1),
                    'columna': getattr(instr, 'columna', -1)
                })
        # Si no hubo break/continue, no retorna nada especial

    def __str__(self):
        return "\n".join(str(instr) for instr in self.instrucciones)

class While(Expresion):
    _contador = 0

    def __init__(self, condicion, instrucciones):
        self.condicion = condicion
        self.instrucciones = instrucciones
        While._contador += 1
        self.id = While._contador

    def interpret(self):
        st.new_scope(f'while_{self.id}')
        while self.condicion.interpret():
            resultado = self.instrucciones.interpret()
            if isinstance(resultado, Break):
                st.exit_scope()
                return
            elif isinstance(resultado, Continue):
                continue
        st.exit_scope()
    def __str__(self):
        # Representación legible del AST
        return f"while_{self.id}: while ({self.condicion}) {{\n{self.instrucciones}\n}}"

    def __repr__(self):
        return f"While#{self.id}(condicion={self.condicion!r}, instrucciones={self.instrucciones!r})"
    
class If(Expresion):
    _contador = 0

    def __init__(self, condicion, instrucciones_si, instrucciones_sino=None):
        self.condicion = condicion
        self.instrucciones_si = instrucciones_si
        self.instrucciones_sino = instrucciones_sino
        If._contador += 1
        self.id = If._contador

    def interpret(self):
        print(f"Evaluando if ID #{self.id}")
        if self.condicion.interpret():
            st.new_scope(f'if_{self.id}_true')
            print(f"Condición verdadera, ejecutando bloque SI")
            res = self.instrucciones_si.interpret()
            st.exit_scope()
            return res
        elif self.instrucciones_sino:
            st.new_scope(f'if_{self.id}_false')
            print(f"Condición falsa, ejecutando bloque SINO")
            res = self.instrucciones_sino.interpret()
            st.exit_scope()
            return res

    def __str__(self):
        texto = f"if_{self.id}: if ({self.condicion}) {{\n{self.instrucciones_si}\n}}"
        if self.instrucciones_sino:
            texto += f" else {{\n{self.instrucciones_sino}\n}}"
        return texto

    def __repr__(self):
        return f"If#{self.id}(condicion={self.condicion!r}, si={self.instrucciones_si!r}, sino={self.instrucciones_sino!r})"
     
class Instruccion(Expresion):
    def __init__(self, instruccion):
        self.instruccion = instruccion

    def interpret(self):
        return self.instruccion.interpret()
    
    def __str__(self):
        print(self.instruccion)
        return f""
    
class Instrucciones(Expresion):
    def __init__(self, instruccion, instrucciones=None):
        if instrucciones is not None:
            self.instrucciones = instrucciones.instrucciones.copy()
        else:
            self.instrucciones = []
        self.instrucciones.append(instruccion)

    def interpret(self, errores_semanticos=None):
        if errores_semanticos is None:
            errores_semanticos = []
        for instr in self.instrucciones:
            try:
                if hasattr(instr, 'interpret') and instr.interpret.__code__.co_argcount == 2:
                    res = instr.interpret(errores_semanticos)
                else:
                    res = instr.interpret()
                # Si la instrucción es Break o Continue, propágalo inmediatamente
                if isinstance(res, Break) or isinstance(res, Continue):
                    return res
            except Exception as e:
                errores_semanticos.append({
                    'tipo': 'Semántico',
                    'descripcion': str(e),
                    'linea': getattr(instr, 'linea', -1),
                    'columna': getattr(instr, 'columna', -1)
                })
        # Si no hubo break/continue, no retorna nada especial

    def __str__(self):
        return "\n".join(str(instr) for instr in self.instrucciones)

class Distinto(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() != self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} != {self.derecha})"

    def __repr__(self):
        return f"Distinto({self.izquierda!r}, {self.derecha!r})"
    
#Ciclo for 

class For(Expresion):
    _contador = 0

    def __init__(self, asignacion, condicion, actualizacion, instrucciones):
        self.asignacion = asignacion             
        self.condicion = condicion                
        self.actualizacion = actualizacion        
        self.instrucciones = instrucciones        
        For._contador += 1
        self.id = For._contador

    def interpret(self):
        print(f"Ejecutando for ID #{self.id}")
        st.new_scope(f'for_{self.id}')  
        
        self.asignacion.interpret()  
        while self.condicion.interpret():  
            resultado = self.instrucciones.interpret()
            if isinstance(resultado, list):
                for r in resultado:
                    if isinstance(r, Break):
                        st.exit_scope()
                        return
                    if isinstance(r, Continue):
                        break
            elif isinstance(resultado, Break):
                st.exit_scope()
                return
            elif isinstance(resultado, Continue):
                self.actualizacion.interpret()
                continue
            self.actualizacion.interpret()  
        st.exit_scope()  

    def __str__(self):
        return f"for_{self.id}: for ({self.asignacion}; {self.condicion}; {self.actualizacion}) {{\n{self.instrucciones}\n}}"

    def __repr__(self):
        return f"For#{self.id}(asignacion={self.asignacion!r}, condicion={self.condicion!r}, actualizacion={self.actualizacion!r}, instrucciones={self.instrucciones!r})"
    
class DoWhile(Expresion):
    _contador = 0

    def __init__(self, instrucciones, condicion):
        self.instrucciones = instrucciones
        self.condicion = condicion
        DoWhile._contador += 1
        self.id = DoWhile._contador

    def interpret(self):
        st.new_scope(f'dowhile_{self.id}')
        while True:
            resultado = self.instrucciones.interpret()
            if isinstance(resultado, Break):
                st.exit_scope()
                return
            elif isinstance(resultado, Continue):
                pass  # Solo salta a la condición
            if not self.condicion.interpret():
                break
        st.exit_scope()

    def __str__(self):
        return f"do_while_{self.id}: do {{\n{self.instrucciones}\n}} while ({self.condicion});"

    def __repr__(self):
        return f"DoWhile#{self.id}(instrucciones={self.instrucciones!r}, condicion={self.condicion!r})"
    
class Break(Expresion):
    def interpret(self):
        return self
    def __str__(self):
        return "break"

class Continue(Expresion):
    def interpret(self):
        return self
    def __str__(self):
        return "continue"

# Clases para la sentencia Switch
class Switch(Expresion):
    _contador = 0

    def __init__(self, expresion, casos, caso_default=None):
        self.expresion = expresion
        self.casos = casos 
        self.caso_default = caso_default
        Switch._contador += 1
        self.id = Switch._contador

    def interpret(self):
        valor = self.expresion.interpret()
        print(f"Evaluando switch ID #{self.id} con valor {valor}")
        st.new_scope(f'switch_{self.id}')
        ejecutado = False

        for caso in self.casos:
            if caso.valor.interpret() == valor:
                caso.interpret()
                ejecutado = True
                break  

        if not ejecutado and self.caso_default:
            print(f"No hubo coincidencia, ejecutando default")
            self.caso_default.interpret()

        st.exit_scope()

    def __str__(self):
        texto = f"switch_{self.id}: switch ({self.expresion}) {{\n"
        for caso in self.casos:
            texto += f"  {caso}\n"
        if self.caso_default:
            texto += f"  {self.caso_default}\n"
        texto += "}"
        return texto

    def __repr__(self):
        return f"Switch#{self.id}(expresion={self.expresion!r}, casos={self.casos!r}, default={self.caso_default!r})"

class Case(Expresion):
    def __init__(self, valor, instrucciones):
        self.valor = valor
        self.instrucciones = instrucciones

    def interpret(self):
        print(f"Ejecutando case con valor {self.valor}")
        self.instrucciones.interpret()

    def __str__(self):
        return f"case {self.valor}: {{\n{self.instrucciones}\n}}"

    def __repr__(self):
        return f"Case(valor={self.valor!r}, instrucciones={self.instrucciones!r})"

class Default(Expresion):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def interpret(self):
        print(f"Ejecutando default")
        self.instrucciones.interpret()

    def __str__(self):
        return f"default: {{\n{self.instrucciones}\n}}"

    def __repr__(self):
        return f"Default(instrucciones={self.instrucciones!r})"
# Aqui terminan las Clases para la Sentencia Switch.

class Vector(Expresion):
    def __init__(self, tipo, identificador, dimensiones, valores=None, linea=None, columna=None):
        self.tipo = tipo
        self.identificador = identificador
        self.dimensiones = dimensiones  # Lista de enteros [2, 2] para 2x2
        self.valores = valores  # Lista anidada de valores [[1,2],[1,5]]
        self.linea = linea
        self.columna = columna

    def interpret(self):
        # Verificar si la variable ya está declarada
        if self.identificador in tabla_variables:
            raise Exception(f"Error semántico: Vector '{self.identificador}' ya ha sido declarado.")

        # Validar dimensiones
        for dim in self.dimensiones:
            if not isinstance(dim, int) or dim <= 0:
                raise Exception(f"Error: Las dimensiones del vector deben ser números enteros positivos")

        # Crear estructura del vector
        if self.valores is None:
            # Solo declaración, inicializar con valores por defecto
            vector_data = self._crear_vector_vacio(self.dimensiones, self.tipo)
        else:
            # Declaración con inicialización
            vector_data = self._validar_y_crear_vector(self.valores, self.dimensiones, self.tipo)

        # Guardar en la tabla de variables con metadatos
        tabla_variables[self.identificador] = {
            'tipo': 'vector',
            'subtipo': self.tipo,
            'dimensiones': self.dimensiones,
            'data': vector_data
        }

        return f"Vector[{self.tipo}] {self.identificador} declarado."

    def _crear_vector_vacio(self, dimensiones, tipo):
        """Crea un vector vacío con valores por defecto según el tipo"""
        if len(dimensiones) == 1:
            if tipo == "int":
                return [0] * dimensiones[0]
            elif tipo == "float":
                return [0.0] * dimensiones[0]
            elif tipo == "char":
                return ['\0'] * dimensiones[0]
            elif tipo == "string":
                return [""] * dimensiones[0]
            elif tipo == "bool":
                return [False] * dimensiones[0]
        else:
            return [self._crear_vector_vacio(dimensiones[1:], tipo) for _ in range(dimensiones[0])]

    def _validar_y_crear_vector(self, valores, dimensiones, tipo):
        """Valida y crea el vector con los valores proporcionados"""
        if len(dimensiones) == 1:
            # Vector unidimensional
            if len(valores) != dimensiones[0]:
                raise Exception(f"Error: Se esperaban {dimensiones[0]} elementos, se recibieron {len(valores)}")
            
            vector_data = []
            for valor in valores:
                valor_interpretado = valor.interpret() if hasattr(valor, 'interpret') else valor
                vector_data.append(self._validar_tipo(valor_interpretado, tipo))
            return vector_data
        else:
            # Vector multidimensional
            if len(valores) != dimensiones[0]:
                raise Exception(f"Error: Se esperaban {dimensiones[0]} filas, se recibieron {len(valores)}")
            
            vector_data = []
            for fila in valores:
                if not isinstance(fila, list):
                    raise Exception(f"Error: Se esperaba una lista para la fila del vector multidimensional")
                vector_data.append(self._validar_y_crear_vector(fila, dimensiones[1:], tipo))
            return vector_data

    def _validar_tipo(self, valor, tipo_esperado):
        """Valida que el valor sea del tipo correcto"""
        def obtener_tipo(val):
            if isinstance(val, bool):
                return "bool"
            elif isinstance(val, int):
                return "int"
            elif isinstance(val, float):
                return "float"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "char"
                return "string"
            return "desconocido"

        tipo_actual = obtener_tipo(valor)
        
        if tipo_esperado == tipo_actual:
            return valor
        elif tipo_esperado == "float" and tipo_actual == "int":
            return float(valor)
        else:
            raise Exception(f"Error: Tipo incompatible. Se esperaba {tipo_esperado}, se recibió {tipo_actual}")

    def __str__(self):
        dimensiones_str = ",".join(map(str, self.dimensiones))
        if self.valores:
            return f"Vector[{self.tipo}] {self.identificador}({dimensiones_str}) = {self.valores}"
        else:
            return f"Vector[{self.tipo}] {self.identificador}({dimensiones_str});"

    def __repr__(self):
        return f"Vector(tipo={self.tipo!r}, identificador={self.identificador!r}, dimensiones={self.dimensiones!r}, valores={self.valores!r})"

class AccesoVector(Expresion):
    def __init__(self, identificador, indices):
        self.identificador = identificador
        self.indices = indices  # Lista de expresiones que representan los índices

    def interpret(self):
        if self.identificador not in tabla_variables:
            raise Exception(f"Error: Vector '{self.identificador}' no ha sido declarado")

        vector_info = tabla_variables[self.identificador]
        if vector_info['tipo'] != 'vector':
            raise Exception(f"Error: '{self.identificador}' no es un vector")

        # Interpretar índices
        indices_interpretados = []
        for indice in self.indices:
            valor_indice = indice.interpret()
            if not isinstance(valor_indice, int):
                raise Exception(f"Error: Los índices del vector deben ser números enteros")
            if valor_indice < 0:
                raise Exception(f"Error: Los índices del vector no pueden ser negativos")
            indices_interpretados.append(valor_indice)

        # Validar número de dimensiones
        if len(indices_interpretados) != len(vector_info['dimensiones']):
            raise Exception(f"Error: Se esperaban {len(vector_info['dimensiones'])} índices, se recibieron {len(indices_interpretados)}")

        # Acceder al elemento
        data = vector_info['data']
        for i, indice in enumerate(indices_interpretados):
            if indice >= vector_info['dimensiones'][i]:
                raise Exception(f"Error: Índice {indice} fuera de rango para la dimensión {i+1} (tamaño: {vector_info['dimensiones'][i]})")
            data = data[indice]

        return data

    def __str__(self):
        indices_str = "][".join(str(indice) for indice in self.indices)
        return f"{self.identificador}[{indices_str}]"

    def __repr__(self):
        return f"AccesoVector(identificador={self.identificador!r}, indices={self.indices!r})"

class AsignacionVector(Expresion):
    def __init__(self, identificador, indices, valor):
        self.identificador = identificador
        self.indices = indices
        self.valor = valor

    def interpret(self):
        if self.identificador not in tabla_variables:
            raise Exception(f"Error: Vector '{self.identificador}' no ha sido declarado")

        vector_info = tabla_variables[self.identificador]
        if vector_info['tipo'] != 'vector':
            raise Exception(f"Error: '{self.identificador}' no es un vector")

        # Interpretar índices
        indices_interpretados = []
        for indice in self.indices:
            valor_indice = indice.interpret()
            if not isinstance(valor_indice, int):
                raise Exception(f"Error: Los índices del vector deben ser números enteros")
            if valor_indice < 0:
                raise Exception(f"Error: Los índices del vector no pueden ser negativos")
            indices_interpretados.append(valor_indice)

        # Validar número de dimensiones
        if len(indices_interpretados) != len(vector_info['dimensiones']):
            raise Exception(f"Error: Se esperaban {len(vector_info['dimensiones'])} índices, se recibieron {len(indices_interpretados)}")

        # Interpretar valor a asignar
        valor_interpretado = self.valor.interpret()

        # Validar tipo
        tipo_esperado = vector_info['subtipo']
        def obtener_tipo(val):
            if isinstance(val, bool):
                return "bool"
            elif isinstance(val, int):
                return "int"
            elif isinstance(val, float):
                return "float"
            elif isinstance(val, str):
                if len(val) == 1:
                    return "char"
                return "string"
            return "desconocido"

        tipo_actual = obtener_tipo(valor_interpretado)
        if tipo_esperado != tipo_actual and not (tipo_esperado == "float" and tipo_actual == "int"):
            raise Exception(f"Error: Tipo incompatible. Se esperaba {tipo_esperado}, se recibió {tipo_actual}")

        if tipo_esperado == "float" and tipo_actual == "int":
            valor_interpretado = float(valor_interpretado)

        # Navegar hasta el elemento y asignar
        data = vector_info['data']
        for i, indice in enumerate(indices_interpretados[:-1]):
            if indice >= vector_info['dimensiones'][i]:
                raise Exception(f"Error: Índice {indice} fuera de rango para la dimensión {i+1}")
            data = data[indice]

        # Asignar el último índice
        ultimo_indice = indices_interpretados[-1]
        if ultimo_indice >= vector_info['dimensiones'][-1]:
            raise Exception(f"Error: Índice {ultimo_indice} fuera de rango para la última dimensión")
        
        data[ultimo_indice] = valor_interpretado
        return valor_interpretado

    def __str__(self):
        indices_str = "][".join(str(indice) for indice in self.indices)
        return f"{self.identificador}[{indices_str}] = {self.valor}"

    def __repr__(self):
        return f"AsignacionVector(identificador={self.identificador!r}, indices={self.indices!r}, valor={self.valor!r})"
