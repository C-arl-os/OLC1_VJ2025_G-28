import ply.yacc as yacc
from lexer import tokens
from nodes.ast_nodes import Numero, Suma, Resta

# Precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
)

def p_instrucciones(t):
    '''instrucciones : instruccion instrucciones
                     | instruccion'''
    pass

def p_instruccion(t):
    '''instruccion : comentario_una_linea
                   | comentario_multi_linea
                   | declaracion_variable'''
    pass


def p_comentario_una_linea(t):
    'comentario_una_linea : C_UNA_LINEA COMENTARIO'
    print(f'Apertura Comentario Unico : {t[1]}')
    print(f'Comentario: {t[2]}')

def p_comentario_multi_linea(t):
    'comentario_multi_linea : C_MULTI_APERTURA COMENTARIO_MULTI C_MULTI_CIERRE'
    print(f'Apertura Comentario: {t[1]}')
    print(f'Comentario: {t[2]}')
    print(f'Cierre Comentario: {t[3]}')

def p_declaracion_variable(t):
    '''declaracion_variable : INT ID IGUAL NUMERO PUNTO_Y_COMA
                            | FLOAT ID IGUAL DECIMAL PUNTO_Y_COMA
                            | STR ID IGUAL STRING PUNTO_Y_COMA
                            | BOOL ID IGUAL booleana PUNTO_Y_COMA
                            | CHAR ID IGUAL CHAR_LITERAL PUNTO_Y_COMA'''

    tipo = t[1]
    nombre = t[2]
    valor = t[4].interpret() if hasattr(t[4], 'interpret') else t[4]  # Evaluar si es nodo

    error = False

    if tipo == 'int' and not isinstance(valor, int):
        error = True
    elif tipo == 'float' and not isinstance(valor, float):
        error = True
    elif tipo == 'bool' and not isinstance(valor, bool):
        error = True
    elif tipo == 'str' and not isinstance(valor, str):
        error = True
    elif tipo == 'char' and not (isinstance(valor, str) and len(valor) == 1):
        error = True

    if error:
        print(f"Error de tipo: No se puede asignar '{valor}' a una variable de tipo '{tipo}'")
    else:
        print(f" Declaración válida: variable '{nombre}' de tipo '{tipo}' con valor '{valor}'")

def p_booleana(p):
    '''booleana : TRUE
                 | FALSE'''
    p[0] = True if p[1] == 'true' else False



start = 'instrucciones'

def p_expresion_numero(p):
    'expresion : NUMERO'
    # Creamos un nodo hoja con el valor entero
    p[0] = Numero(p[1])

def p_expresion_suma(p):
    'expresion : expresion MAS expresion'
    # Creamos un nodo Suma con sus hijos
    p[0] = Suma(p[1], p[3])

def p_expresion_resta(p):
    'expresion : expresion MENOS expresion'
    p[0] = Resta(p[1], p[3])

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de entrada inesperado")

# Construimos el parser
parser = yacc.yacc()