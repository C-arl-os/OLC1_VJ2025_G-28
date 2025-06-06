import ply.yacc as yacc
from lexer import tokens
from nodes.ast_nodes import  Resta
from nodes.Nodo import Expresion
from nodes.Numero import Numero
from nodes.Suma import Suma
from nodes.Multi import Multi
from nodes.Asignacion import Asignacion
from nodes.Div import Div

# Precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    
)


def p_declaracion_asignacion(p):
    'expresion : INT ID IGUAL expresion PTCOMA'
    p[0] = Asignacion(p[2], p[4])

def p_expresion_entero(p):
    'expresion : ENTERO'
    p[0] = Numero(p[1])

def p_expresion_decimal(p):
    'expresion : FLOTANTE'
    p[0] = Numero(p[1])

def p_expresion_suma(p):
    'expresion : expresion MAS expresion'
    p[0] = Suma(p[1], p[3])

def p_expresion_resta(p):
    'expresion : expresion MENOS expresion'
    p[0] = Resta(p[1], p[3])

def p_expresion_multi(p):
    'expresion : expresion POR expresion'
    p[0] = Multi(p[1], p[3])

def p_asignacion(p):
    'expresion : INT PARIZQ expresion PARDER PTCOMA'
    p[0] = p[3]  # Retorna la expresión evaluada

def p_inicio(p):
    'inicio : expresion'
    p[0] = p[1]
    
def p_expresion_div(p):
    'expresion : expresion DIVIDIDO expresion'
    p[0] = Div(p[1], p[3])  # Asegúrate de tener una clase Div igual a Suma o Multi

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de entrada inesperado")

# Construimos el parser
parser = yacc.yacc(start='inicio')
