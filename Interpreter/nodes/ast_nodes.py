from contexto import tabla_variables
from .Nodo import Expresion
from contexto import tabla_variables, salidas_de_impresion
from tabla_simbolos.instancia import symbol_table as st


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

        # Manejo de errores: combinaciones no válidas
        if isinstance(izq, bool) or isinstance(der, bool):
            # Solo se permite booleano + cadena
            if isinstance(izq, str) or isinstance(der, str):
                return str(izq) + str(der)
            else:
                print(f"Error: No se puede sumar tipos inválidos → {type(izq).__name__} + {type(der).__name__}")
                return None

        # Caracter a número (usa ord)
        if isinstance(izq, str) and len(izq) == 1 and not izq.isnumeric():
            izq_val = ord(izq)
        else:
            izq_val = izq

        if isinstance(der, str) and len(der) == 1 and not der.isnumeric():
            der_val = ord(der)
        else:
            der_val = der

        # Reglas de suma
        if isinstance(izq, int) and isinstance(der, int):
            return izq + der
        elif isinstance(izq, (int, float)) and isinstance(der, (int, float)):
            return float(izq) + float(der)
        elif isinstance(izq, (int, float)) and isinstance(der, str) and len(der) > 1:
            return str(izq) + der
        elif isinstance(izq, str) and isinstance(der, (int, float)):
            return izq + str(der)
        elif isinstance(izq, (int, float)) and isinstance(der, str) and len(der) == 1:
            return izq + ord(der)
        elif isinstance(izq, str) and len(izq) == 1 and isinstance(der, (int, float)):
            return ord(izq) + der
        elif isinstance(izq, str) and isinstance(der, str):
            return izq + der
        elif isinstance(izq, str) and isinstance(der, bool):
            return izq + str(der)
        elif isinstance(izq, bool) and isinstance(der, str):
            return str(izq) + der
        elif isinstance(izq, str) and len(izq) == 1 and isinstance(der, str) and len(der) == 1:
            return izq + der  # caracter + caracter = cadena
        else:
            print(f"Error: No se puede sumar tipos inválidos → {type(izq).__name__} + {type(der).__name__}")
            return None

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

        # Caso caracter - caracter (no válido)
        if isinstance(izq, str) and isinstance(der, str) and len(izq) == 1 and len(der) == 1:
            print("Error: No se puede restar caracter - caracter")
            return None

        # Convertir caracteres a código ASCII si es necesario
        if isinstance(izq, str) and len(izq) == 1:
            izq = ord(izq)
        if isinstance(der, str) and len(der) == 1:
            der = ord(der)

        # Realizar la resta con promoción de tipos
        resultado = izq - der
        return resultado

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

        # Validar si ambos son caracteres (no válido)
        if isinstance(izq, str) and isinstance(der, str) and len(izq) == 1 and len(der) == 1:
            print("Error: No se puede multiplicar caracter * caracter")
            return None

        # Convertir caracteres a ASCII si es necesario
        if isinstance(izq, str) and len(izq) == 1:
            izq = ord(izq)
        if isinstance(der, str) and len(der) == 1:
            der = ord(der)

        resultado = izq * der

        # Promoción de tipo
        if isinstance(izq, float) or isinstance(der, float):
            return float(resultado)
        else:
            return int(resultado)

    def __str__(self):
        return f"({self.izquierda} * {self.derecha})"

    def __repr__(self):
        return f"Multiplicacion({self.izquierda!r}, {self.derecha!r})"

class Division(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izquierda = self.izquierda.interpret()
        derecha = self.derecha.interpret()

        if isinstance(izquierda, str):
            izquierda = ord(izquierda)
        if isinstance(derecha, str):
            derecha = ord(derecha)

        try:
            resultado = izquierda / derecha
        except ZeroDivisionError:
            print("Error: División por cero.")
            return None

        # Validaciones por tipo
        if isinstance(self.izquierda, Caracter) and isinstance(self.derecha, Caracter):
            print("Error: No se puede dividir caracter / caracter")
            return None

        return float(resultado)

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
        
        resultado = base_val ** exponente_val

        if isinstance(base_val, int) and isinstance(exponente_val, int):
            return int(resultado)
        else:
            return float(resultado)

    def __str__(self):
        return f"({self.base} ** {self.exponente})"

    def __repr__(self):
        return f"Potencia({self.base!r}, {self.exponente!r})"

class Modulo(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        izq_val = self.izquierda.interpret()
        der_val = self.derecha.interpret()
        try:
            resultado = izq_val % der_val
            return float(resultado)  # Siempre se convierte a decimal según la tabla
        except ZeroDivisionError:
            print("Error: módulo por cero.")
            return None

    def __str__(self):
        return f"({self.izquierda} % {self.derecha})"

    def __repr__(self):
        return f"Modulo({self.izquierda!r}, {self.derecha!r})"

class Negativo(Expresion):
    def __init__(self, expresion):
        self.expresion = expresion

    def interpret(self):
        return -self.expresion.interpret()

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
        if self.nombre in tabla_variables:
            return tabla_variables[self.nombre]
        else:
            raise Exception(f"Variable '{self.nombre}' no ha sido definida")

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Identificador('{self.nombre}')"

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
#operadores
# ...existing code...

class MayorIgual(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() >= self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} >= {self.derecha})"

    def __repr__(self):
        return f"MayorIgual({self.izquierda!r}, {self.derecha!r})"

class MenorIgual(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() <= self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} <= {self.derecha})"

    def __repr__(self):
        return f"MenorIgual({self.izquierda!r}, {self.derecha!r})"

class MenorQue(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() < self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} < {self.derecha})"

    def __repr__(self):
        return f"MenorQue({self.izquierda!r}, {self.derecha!r})"

class MayorQue(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() > self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} > {self.derecha})"

    def __repr__(self):
        return f"MayorQue({self.izquierda!r}, {self.derecha!r})"

class Igual(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return self.izquierda.interpret() == self.derecha.interpret()

    def __str__(self):
        return f"({self.izquierda} == {self.derecha})"

    def __repr__(self):
        return f"Igual({self.izquierda!r}, {self.derecha!r})"

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
        self. derecha = derecha

    def interpret(self):
        return bool(self.izquierda.interpret()) or bool(self.derecha.interpret())
    
    def __repr__(self):
        return f'({self.izquierda} || {self.derecha})'   

class AndLogicoNode:
    def __init__(self, izquierda, derecha):
        self. izquierda = izquierda
        self.derecha = derecha

    def interpret(self):
        return bool(self.izquierda.interpret()) and bool(self.derecha.interpret())
    
    def __str__(self):
        return f"({self.izquierda} && {self.derecha})"

class NotLogicoNode:
    def __init__(self, expr):
        self.expr = expr

    def interpret(self):
        return not self.expr.interpret()
    
    def __str__(self):
        return f"(!{self.expr})"

class XorLogicoNode:
    def __init__(self, izquierda, derecha):
        self. izquierda = izquierda
        self. derecha = derecha

    def interpret(self):
        return bool(self.izquierda.interpret()) ^ bool(self.derecha.interpret())
    
    def __str__(self):
        return f"({self. izquierda} ^ {self.derecha})"

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

    def interpret(self):
        results = []
        for instr in self.instrucciones:
            results.append(instr.interpret())
        return results

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
        print(f"Ejecutando while ID #{self.id}")
        while self.condicion.interpret():
            self.instrucciones.interpret()
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
            self.instrucciones_si.interpret()
            st.exit_scope()
        elif self.instrucciones_sino:
            st.new_scope(f'if_{self.id}_false')
            print(f"Condición falsa, ejecutando bloque SINO")
            self.instrucciones_sino.interpret()
            st.exit_scope()

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

    def interpret(self):
        results = []
        for instr in self.instrucciones:
            results.append(instr.interpret())
        return results

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
            self.instrucciones.interpret() 
            self.actualizacion.interpret()  
        st.exit_scope()  

    def __str__(self):
        return f"for_{self.id}: for ({self.asignacion}; {self.condicion}; {self.actualizacion}) {{\n{self.instrucciones}\n}}"

    def __repr__(self):
        return f"For#{self.id}(asignacion={self.asignacion!r}, condicion={self.condicion!r}, actualizacion={self.actualizacion!r}, instrucciones={self.instrucciones!r})"