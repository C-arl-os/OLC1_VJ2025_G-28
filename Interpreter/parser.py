import ply.ply.yacc as yacc
from lexer import tokens
from nodes.ast_nodes import Numero, Suma, Resta,Asignacion, Identificador, Decimal, Caracter, Cadena, Boleano

# Precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    
)

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


def p_asignacion(p):
    '''expresion : tipo ID ASIGNACION expresion PTCOMA'''
    p[0] = Asignacion(p[1], p[2], p[4])

def p_tipo(p):
    '''tipo : ID'''
    p[0] = p[1]  

def p_expresion_decimal(p):
    'expresion : DECIMAL'
    p[0] = Decimal(p[1])

def p_expresion_caracter(p):
    'expresion : CARACTER'
    p[0] = Caracter(p[1])

def p_expresion_cadena(p):
    'expresion : CADENA'
    p[0] = Cadena(p[1])

def p_expresion_boleano(p):
    'expresion : BOLEANO'
    p[0] = Boleano(p[1])

def p_expresion_id(p):
    'expresion : ID'
    p[0] = Identificador(p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de entrada inesperado")

# Construimos el parser
parser = yacc.yacc()
