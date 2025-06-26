import ply.yacc as yacc
from lexer import tokens, errores_lexicos, calcular_columna
from nodes.ast_nodes import Numero, Decimal, Boleano, Caracter, Cadena, Identificador, Asignacion, Suma, Resta, Multiplicacion, Division,Potencia,Modulo,Negativo, Println, ErrorPrintln
from nodes.ast_nodes import MayorIgual, MenorIgual, MenorQue, MayorQue, Igual,Incremento, Decremento, Instruccion,Instrucciones,While, Distinto, If, For
from nodes.ast_nodes import OrLogicoNode, AndLogicoNode, NotLogicoNode, XorLogicoNode, DoWhile, Declaracion,Break, Continue
from nodes.ast_nodes import Switch,Case,Default, Seno, Coseno, Inversa

from nodes.ast_nodes import Vector, AccesoVector, AsignacionVector, VectorShuffle, VectorSort
from nodes.ast_nodes import Procedimiento, LlamadaProcedimiento

comentarios = []
errores_sintacticos = []
# Precedencia
precedence = (
    ('right', 'NOT_LOGICO'),  
    ('left', 'OR_LOGICO'),  
    ('left', 'AND_LOGICO'),  
    ('left', 'XOR_LOGICO'),  
    ('left', 'GE', 'LE', 'LT', 'GT', 'EQ', 'NE'),   # Comparaciones
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right', 'UMINUS'),
    ('left', 'CORIZQ', 'CORDER'),
)

# Regla para expresiones simples
def p_inicio(p):
    '''inicio : lista_expresiones
              | expresion
              | comentario_una_linea
              | comentario_multi_linea'''
    p[0] = p[1]


def p_lista_expresiones_unica(p):
    '''lista_expresiones : expresion PTCOMA
                         | expresion'''
    # sólo “expresion ;” o expresión final SIN ;
    p[0] = Instrucciones(p[1])

def p_lista_expresiones_append(p):
    'lista_expresiones : lista_expresiones expresion PTCOMA'
    # lista previa + expresión con ;
    p[0] = Instrucciones(p[2], p[1])

def p_lista_expresiones_sin_punto(p):
    'lista_expresiones : lista_expresiones expresion'
    # lista previa + expresión final SIN ;
    p[0] = Instrucciones(p[2], p[1])
#Matriz 


#ciclo while 


def p_expresion_while(p):
    'expresion : WHILE PARIZQ expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER'
    p[0] = While(p[3], p[6])
    
#ciclo do while

def p_expresion_do_while(p):
    'expresion : DO LLAVE_IZQ lista_expresiones LLAVE_DER WHILE PARIZQ expresion PARDER PTCOMA'
    p[0] = DoWhile(p[3], p[7])
#if
# if sin else
def p_expresion_if(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER'
    p[0] = If(p[3], p[6])

# if con else
def p_expresion_if_else(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER ELSE LLAVE_IZQ lista_expresiones LLAVE_DER'
    p[0] = If(p[3], p[6], p[10])

# if con else if
def p_expresion_if_elseif(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER ELSE expresion'
    p[0] = If(p[3], p[6], p[9])  # p[9] es otra expresión if (recursiva)

def p_expresion_entero(p):
    'expresion : ENTERO'
    p[0] = Numero(p[1])

def p_expresion_decimal(p):
    
    'expresion : DECIMAL'
    p[0] = Decimal(p[1])

#ciclo for declarando variable
def p_expresion_for_con_tipo(p):
    '''expresion : FOR PARIZQ tipo ID ASIGNACION expresion PTCOMA expresion PTCOMA expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER'''
    asignacion = Asignacion(p[3], p[4], p[6])  # tipo, id, valor
    condicion = p[8]
    actualizacion = p[10]
    instrucciones = p[13]
    p[0] = For(asignacion, condicion, actualizacion, instrucciones)


#ciclo for con una variable ya declarada
def p_expresion_for_sin_tipo(p):
    '''expresion : FOR PARIZQ ID ASIGNACION expresion PTCOMA expresion PTCOMA expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER'''
    asignacion = Asignacion(None, p[3], p[5])  # Sin tipo
    condicion = p[7]
    actualizacion = p[9]
    instrucciones = p[12]
    p[0] = For(asignacion, condicion, actualizacion, instrucciones)

#booleanos
def p_expresion_true(p):
    'expresion : TRUE'
    p[0] = Boleano(True)

def p_expresion_false(p):
    'expresion : FALSE'
    p[0] = Boleano(False)

def p_expresion_caracter(p):
    'expresion : CARACTER'
    p[0] = Caracter(p[1])

def p_expresion_cadena(p):
    'expresion : CADENA'
    p[0] = Cadena(p[1])

def p_expresion_id(p):
    'expresion : ID'
    p[0] = Identificador(p[1])

# aqui va esta regla por que causa conflicto con la suma y resta.
def p_expresion_negativa(p):
    'expresion : MENOS expresion %prec UMINUS'
    p[0] = Negativo(p[2])

def p_expresion_suma(p):
    'expresion : expresion MAS expresion'
    p[0] = Suma(p[1], p[3])

def p_expresion_resta(p):
    'expresion : expresion MENOS expresion'
    p[0] = Resta(p[1], p[3])

def p_expresion_multiplicacion(p):
    'expresion : expresion POR expresion'
    p[0] = Multiplicacion(p[1], p[3])

def p_expresion_division(p):
    'expresion : expresion DIVIDIDO expresion'
    p[0] = Division(p[1], p[3])

def p_expresion_potencia(p):
    'expresion : expresion POTENCIA expresion'
    p[0] = Potencia(p[1], p[3])

def p_expresion_seno(p):
    'expresion : SENO PARIZQ expresion PARDER'
    p[0] = Seno(p[3])

def p_expresion_coseno(p):
    'expresion : COSENO PARIZQ expresion PARDER'
    p[0] = Coseno(p[3])

def p_expresion_inverso(p):
    'expresion : INV PARIZQ expresion PARDER'
    p[0] = Inversa(p[3])

def p_expresion_modulo(p):
    'expresion : expresion MODULO expresion'
    p[0] = Modulo(p[1], p[3])

def p_declaracion(p):
    'expresion : tipo ID PTCOMA'
    texto_fuente = p.lexer.lexdata  # Acceso al texto fuente completo
    columna = calcular_columna(p.lexpos(2), texto_fuente)
    p[0] = Declaracion(p[1], p[2], p.lineno(2), columna)

def p_asignacion(p):
    'expresion : ID ASIGNACION expresion PTCOMA'
    p[0] = Asignacion(None, p[1], p[3])


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''
    p[0] = p[1]

# === Errores manejables con punto y coma ===
# ===> Error para print
# ===> Error para una cadena en caso no lleve comillas
def p_expresion_println(p):
    'expresion : PRINTLN PARIZQ expresion PARDER PTCOMA'
    
    # Solo generar error para la palabra reservada 'print'
    if isinstance(p[3], Identificador) and p[3].nombre == 'print':
        p[0] = ErrorPrintln("print", "'print' en lugar de 'println'", p.lineno(1), p.lexpos(1))
    else:
        # Permitir tanto cadenas como identificadores (variables)
        p[0] = Println(p[3])

# === Errores manejables sin punto y coma ===
# ===> Error para print
# ===> Error para una cadena en caso no lleve comillas
# ===> Error para punto y coma
def p_expresion_println_sin_ptcoma(p):
    'expresion : PRINTLN PARIZQ expresion PARDER'
    errores_sintacticos.append({
        'tipo': 'Sintáctico',
        'descripcion': "Falta punto y coma",
        'linea': p.lineno(1),
        'columna': p.lexpos(1)
        #Si ya entro aqui que ya no ejecute la ultima linea
    })
    # === Esto es para mostrar el error en el semantico ===
    p[0] = ErrorPrintln("println falta ';'", p.lineno(1), p.lexpos(1))

# === Errores manejables con multiples ID (oraciones sin comillas) ===

# === Errores manejables con multiples ID (oraciones sin comillas) con punto y coma ===
# ===> La entrada aceptada es: println(probando la catidad de id); ---> El error es el multiple ID
# ===> La entrada aceptada es: print(probando la catidad de id); ---> El error es la palabra print y el multiple ID

# !!!!!!!!!!!!!!!!! No reconoce PRINT print(no funciona la parte de oraciones 2); !!!!!!!!!!!!!!!!!!!!!!!!!
def p_expresion_oraciones_println(p):
    'expresion : PRINTLN PARIZQ oraciones PARDER PTCOMA'
    
    # Caso de múltiples ID → error semántico
    if isinstance(p[3], list) and len(p[3]) > 1:
        p[0] = ErrorPrintln("Se detectaron múltiples ID sin comillas", p.lineno(1), p.lexpos(1))

    # Caso válido: un solo ID
    else:
        p[0] = Println(p[3])


# === Errores manejables con multiples ID (oraciones sin comillas) sin punto y coma ===
# ===> La entrada aceptada es: println(probando la catidad de id) ---> El error es el multiple ID y el punto y coma
# ===> La entrada aceptada es: print(probando la catidad de id) ---> El error es la palabra print, multiple ID y el punto y coma

# !!!!!!!!!!!!!!!!! No reconoce PRINT print(no funciona la parte de oraciones 2) !!!!!!!!!!!!!!!!!!!!!!!!!
def p_expresion_oraciones_println_sin_ptcoma(p):
    'expresion : PRINTLN PARIZQ oraciones PARDER'

    errores_sintacticos.append({
        'tipo': 'Sintáctico',
        'descripcion': "Falta punto y coma",
        'linea': p.lineno(1),
        'columna': p.lexpos(1)
    })

    # Generar error semántico también por múltiples ID
    if isinstance(p[3], list) and len(p[3]) > 1:
        p[0] = ErrorPrintln("Cadena sin comillas + falta ';'", p.lineno(1), p.lexpos(1))
    else:
        p[0] = ErrorPrintln("println falta ';'", p.lineno(1), p.lexpos(1))

# === Detectan N cantidad de ID (oraciones sin comillas dentro de un println)
def p_oraciones_lista(p):
    'oraciones : oraciones ID'
    p[0] = [*p[1], p[2]]

def p_oraciones_id(p):
    'oraciones : ID'
    p[0] = [p[1]]

# Declara la asignacion
def p_declaracion_asignacion(p):
    'expresion : tipo ID ASIGNACION expresion PTCOMA'
    p[0] = Asignacion(p[1], p[2], p[4])

# Operadores lógicos
def p_expresion_or_logico(p):
    'expresion : expresion OR_LOGICO expresion'
    p[0] = OrLogicoNode(p[1], p[3])

def p_expresion_and_logico(p):
    'expresion : expresion AND_LOGICO expresion'
    p[0] = AndLogicoNode(p[1], p[3])

def p_expresion_not_logico(p):
    'expresion : NOT_LOGICO expresion'
    p[0] = NotLogicoNode(p[2])

def p_expresion_xor_logico(p):
    'expresion : expresion XOR_LOGICO expresion'
    p[0] = XorLogicoNode(p[1], p[3])
    
def p_expresion_break(p):
    'expresion : BREAK PTCOMA'
    p[0] = Break()

def p_expresion_continue(p):
    'expresion : CONTINUE PTCOMA'
    p[0] = Continue()
# …existing code…

#operadores

def p_expresion_comparacion(p):
    '''expresion : expresion GE expresion
                 | expresion LE expresion
                 | expresion LT expresion
                 | expresion GT expresion
                 | expresion EQ expresion
                 | expresion NE expresion'''
    if p[2] == '>=':
        p[0] = MayorIgual(p[1], p[3])
    elif p[2] == '<=':
        p[0] = MenorIgual(p[1], p[3])
    elif p[2] == '<':
        p[0] = MenorQue(p[1], p[3])
    elif p[2] == '>':
        p[0] = MayorQue(p[1], p[3])
    elif p[2] == '==':
        p[0] = Igual(p[1], p[3])
    elif p[2] == '!=':
        p[0] = Distinto(p[1], p[3])  #
        
#INCREMENTO Y DEREMENTO 
def p_expresion_incremento(p):
    'expresion : ID INCREMENTO'
    p[0] = Incremento(Identificador(p[1]))

def p_expresion_decremento(p):
    'expresion : ID DECREMENTO'
    p[0] = Decremento(Identificador(p[1]))
#comentarios
def p_comentario_multi_linea(t):
    'comentario_multi_linea : COMENTARIO_MULTILINEA'
    comentarios.append(f'Comentario Multilínea: {t[1]}')
    print(f'Comentario Multilínea: {t[1]}')
    pass

def p_comentario_una_linea(t):
    'comentario_una_linea : COMENTARIO_UNA_LINEA'
    comentarios.append(f'Comentario de una línea: {t[1]}')
    print(f'Comentario de una línea: {t[1]}')
    pass

# Regla para expresiones entre paréntesis
def p_expresion_parentesis(p):
    'expresion : PARIZQ expresion PARDER'
    p[0] = p[2]

# Reglas para la sentencia de control Switch
def p_expresion_switch(p):
    'expresion : SWITCH PARIZQ expresion PARDER LLAVE_IZQ lista_cases_opt LLAVE_DER'
    p[0] = Switch(p[3], p[6]["casos"], p[6].get("default"))

def p_lista_cases_opt_con_default(p):
    'lista_cases_opt : lista_cases case_default'
    p[0] = {"casos": p[1], "default": p[2]}

def p_lista_cases_opt_sin_default(p):
    'lista_cases_opt : lista_cases'
    p[0] = {"casos": p[1]}

def p_lista_cases_varios(p):
    'lista_cases : lista_cases case'
    p[0] = p[1] + [p[2]]

def p_lista_cases_uno(p):
    'lista_cases : case'
    p[0] = [p[1]]

def p_case(p):
    'case : CASE expresion DOSPUNTOS lista_expresiones'
    p[0] = Case(p[2], p[4])

def p_case_default(p):
    'case_default : DEFAULT DOSPUNTOS lista_expresiones'
    p[0] = Default(p[3])
# Aqui terminan...
# Reglas para manejar bloques vacíos - agregar antes de p_error

# IF con bloque vacío
def p_expresion_if_vacio(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ LLAVE_DER'
    # Bloque vacío = solo continue
    p[0] = If(p[3], Continue())

# WHILE con bloque vacío
def p_expresion_while_vacio(p):
    'expresion : WHILE PARIZQ expresion PARDER LLAVE_IZQ LLAVE_DER'
    p[0] = While(p[3], Continue())

# FOR con bloque vacío (con tipo)
def p_expresion_for_con_tipo_vacio(p):
    '''expresion : FOR PARIZQ tipo ID ASIGNACION expresion PTCOMA expresion PTCOMA expresion PARDER LLAVE_IZQ LLAVE_DER'''
    asignacion = Asignacion(p[3], p[4], p[6])
    p[0] = For(asignacion, p[8], p[10], Continue())

# FOR con bloque vacío (sin tipo)
def p_expresion_for_sin_tipo_vacio(p):
    '''expresion : FOR PARIZQ ID ASIGNACION expresion PTCOMA expresion PTCOMA expresion PARDER LLAVE_IZQ LLAVE_DER'''
    asignacion = Asignacion(None, p[3], p[5])
    p[0] = For(asignacion, p[7], p[9], Continue())

# DO-WHILE con bloque vacío
def p_expresion_do_while_vacio(p):
    'expresion : DO LLAVE_IZQ LLAVE_DER WHILE PARIZQ expresion PARDER PTCOMA'
    p[0] = DoWhile(Continue(), p[6])

# IF-ELSE con bloque SI vacío
def p_expresion_if_else_vacio_si(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ LLAVE_DER ELSE LLAVE_IZQ lista_expresiones LLAVE_DER'
    p[0] = If(p[3], Continue(), p[9])

# IF-ELSE con bloque ELSE vacío
def p_expresion_if_else_vacio_else(p):
    'expresion : IF PARIZQ expresion PARDER LLAVE_IZQ lista_expresiones LLAVE_DER ELSE LLAVE_IZQ LLAVE_DER'
    p[0] = If(p[3], p[6], Continue())

# Lista de expresiones vacía (para casos donde se necesite)
def p_lista_expresiones_vacia(p):
    '''lista_expresiones : '''
    p[0] = Continue()
# Aqui terminan...
def p_expresion_vector_declaracion(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ lista_dimensiones PARDER PTCOMA'
    p[0] = Vector(p[3], p[5], p[7])

def p_expresion_vector_declaracion_shuffle(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ lista_dimensiones PARDER ASIGNACION SHUFFLE PARIZQ ID PARDER PTCOMA'    
    print("RTESTESETSFLKSJFLKSEJFLSKEJF")
    p[0] = VectorShuffle(p[3], p[5], p[7], p[12])

def p_vector_una_dimension(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ ENTERO PARDER ASIGNACION CORIZQ lista_elementos CORDER PTCOMA'
    dimensiones = [p[7]]  # solo una dimensión
    p[0] = Vector(p[3], p[5], dimensiones, p[11])

def p_expresion_vector_declaracion_sort(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ ENTERO PARDER ASIGNACION SORT PARIZQ ID PARDER PTCOMA'
    dimensiones = [p[7]]
    p[0] = VectorSort(p[3], p[5], dimensiones, p[12])

# Declaración de vector con inicialización
def p_expresion_vector_declaracion_inicializacion(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ lista_dimensiones PARDER ASIGNACION lista_valores PTCOMA'    
    p[0] = Vector(p[3], p[5], p[7], p[10])

# Regla para vectores multidimensionales con inicialización compleja
def p_vector_multidimensional_complejo(p):
    'expresion : VECTOR CORIZQ tipo CORDER ID PARIZQ lista_dimensiones PARDER ASIGNACION estructura_multidimensional PTCOMA'
    p[0] = Vector(p[3], p[5], p[7], p[10])

# Estructura multidimensional anidada
def p_estructura_multidimensional(p):
    'estructura_multidimensional : CORIZQ lista_estructuras CORDER'
    p[0] = p[2]

def p_lista_estructuras_multiple(p):
    'lista_estructuras : lista_estructuras COMA elemento_estructura'
    p[0] = p[1] + [p[3]]

def p_lista_estructuras_unica(p):
    'lista_estructuras : elemento_estructura'
    p[0] = [p[1]]

def p_elemento_estructura_anidado(p):
    'elemento_estructura : estructura_multidimensional'
    p[0] = p[1]

def p_elemento_estructura_lista(p):
    'elemento_estructura : CORIZQ lista_elementos CORDER'
    p[0] = p[2]

# ...existing code...
# Lista de dimensiones (números separados por comas)
def p_lista_dimensiones_multiple(p):
    'lista_dimensiones : lista_dimensiones COMA ENTERO'
    p[0] = p[1] + [p[3]]

def p_lista_dimensiones_unica(p):
    'lista_dimensiones : ENTERO'
    p[0] = [p[1]]

# Para la inicialización de vectores multidimensionales, necesitamos ajustar las reglas
def p_lista_valores_multiple(p):
    '''lista_valores : lista_valores COMA fila_vector
                     | lista_valores COMA CORIZQ lista_elementos CORDER'''
    if len(p) == 4:  # lista_valores COMA fila_vector
        p[0] = p[1] + [p[3]]
    else:  # lista_valores COMA CORIZQ lista_elementos CORDER
        p[0] = p[1] + [p[4]]

def p_lista_valores_unica(p):
    '''lista_valores : fila_vector
                     | CORIZQ lista_elementos CORDER'''
    if len(p) == 2:  # fila_vector
        p[0] = [p[1]]
    else:  # CORIZQ lista_elementos CORDER
        p[0] = [p[2]]

def p_fila_vector(p):
    'fila_vector : CORIZQ lista_elementos CORDER'
    p[0] = p[2]

def p_lista_elementos_multiple(p):
    'lista_elementos : lista_elementos COMA expresion'
    p[0] = p[1] + [p[3]]

def p_lista_elementos_unica(p):
    'lista_elementos : expresion'
    p[0] = [p[1]]

# Acceso a elementos de vector - necesita prioridad más baja
def p_expresion_acceso_vector(p):
    'expresion : ID lista_indices'
    # Solo aplicar si realmente hay índices y no es una variable normal
    if len(p[2]) > 0:
        p[0] = AccesoVector(p[1], p[2])
    else:
        p[0] = Identificador(p[1])

# Asignación a elementos de vector
def p_expresion_asignacion_vector(p):
    'expresion : ID lista_indices ASIGNACION expresion PTCOMA'
    p[0] = AsignacionVector(p[1], p[2], p[4])

# Lista de índices
def p_lista_indices_multiple(p):
    'lista_indices : lista_indices CORIZQ expresion CORDER'
    p[0] = p[1] + [p[3]]

def p_lista_indices_unica(p):
    'lista_indices : CORIZQ expresion CORDER'
    p[0] = [p[2]]

# Regla para lista_indices vacía (para evitar conflictos)
def p_lista_indices_vacia(p):
    'lista_indices : '
    p[0] = []

# Regla para procedimientos
# Procedimientos con nombre, parámetros y cuerpo
def p_expresion_procedimiento(p):
    'expresion : PROC ID PARIZQ lista_parametros_opt PARDER LLAVE_IZQ lista_expresiones LLAVE_DER'
    p[0] = Procedimiento(p[2], p[4], p[7])


def p_lista_parametros_opt(p):
    '''lista_parametros_opt : lista_parametros
                           | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_lista_parametros_varios(p):
    'lista_parametros : lista_parametros COMA tipo DOSPUNTOS ID'
    p[0] = p[1] + [(p[3], p[5])]

def p_lista_parametros_uno(p):
    'lista_parametros : tipo DOSPUNTOS ID'
    p[0] = [(p[1], p[3])]

# Regla para llamadas a procedimientos con EXEC
def p_expresion_llamada_procedimiento_exec(p):
    'expresion : EXEC ID PARIZQ lista_argumentos_exec_opt PARDER PTCOMA'
    p[0] = LlamadaProcedimiento(p[2], p[4])

def p_lista_argumentos_exec_opt(p):
    '''lista_argumentos_exec_opt : lista_argumentos_exec
                                 | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_lista_argumentos_exec_varios(p):
    'lista_argumentos_exec : lista_argumentos_exec COMA argumento_exec'
    p[0] = p[1] + [p[3]]

def p_lista_argumentos_exec_uno(p):
    'lista_argumentos_exec : argumento_exec'
    p[0] = [p[1]]

def p_argumento_exec_id(p):
    'argumento_exec : ID'
    p[0] = Identificador(p[1])

def p_argumento_exec_entero(p):
    'argumento_exec : ENTERO'
    p[0] = Numero(p[1])

def p_argumento_exec_decimal(p):
    'argumento_exec : DECIMAL'
    p[0] = Decimal(p[1])

def p_argumento_exec_caracter(p):
    'argumento_exec : CARACTER'
    p[0] = Caracter(p[1])

def p_argumento_exec_cadena(p):
    'argumento_exec : CADENA'
    p[0] = Cadena(p[1])

def p_argumento_exec_true(p):
    'argumento_exec : TRUE'
    p[0] = Boleano(True)

def p_argumento_exec_false(p):
    'argumento_exec : FALSE'
    p[0] = Boleano(False)

def p_lista_argumentos_varios(p):
    'lista_argumentos : lista_argumentos COMA expresion'
    p[0] = p[1] + [p[3]]

def p_lista_argumentos_uno(p):
    'lista_argumentos : expresion'
    p[0] = [p[1]]

# Eliminar la función p_error duplicada y mantener solo esta versión:
def p_error(p):
    if p:
        errores_sintacticos.append({
            'tipo': 'Sintáctico',
            'descripcion': f"Token inesperado '{p.value}'",
            'linea': p.lineno,
            'columna': p.lexpos
        })
        # Panic-mode: descartar hasta ; o }
        while True:
            tok = parser.token()
            if not tok or tok.type in ('PTCOMA','LLAVE_DER'):
                break
        parser.errok()
    else:
        errores_sintacticos.append({
            'tipo': 'Sintáctico',
            'descripcion': 'EOF inesperado',
            'linea': -1,
            'columna': -1
        })


parser = yacc.yacc(start='inicio')