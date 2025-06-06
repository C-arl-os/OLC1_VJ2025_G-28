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
                   | comentario_multi_linea'''
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