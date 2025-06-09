import ply.yacc as yacc
from lexer import tokens
from nodes.ast_nodes import Numero, Decimal, Boleano, Caracter, Cadena, Identificador, Asignacion, Suma, Resta, Multiplicacion, Division,Potencia,Modulo,Negativo, Println
comentarios = []

# Precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right', 'UMINUS'),
)

# Regla para expresiones simples
def p_inicio(p):
    '''inicio : expresion
              | lista_expresiones
              | comentario_una_linea
              | comentario_multi_linea'''
    p[0] = p[1]

def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones expresion PTCOMA
                         | expresion PTCOMA'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_expresion_entero(p):
    'expresion : ENTERO'
    p[0] = Numero(p[1])

def p_expresion_decimal(p):
    'expresion : DECIMAL'
    p[0] = Decimal(p[1])

def p_expresion_boleano(p):
    'expresion : BOLEANO'
    p[0] = Boleano(p[1])

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

def p_expresion_modulo(p):
    'expresion : expresion MODULO expresion'
    p[0] = Modulo(p[1], p[3])

def p_asignacion(p):
    '''expresion : ID ASIGNACION expresion'''
    p[0] = Asignacion(None, p[1], p[3])  

def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''
    p[0] = p[1]

def p_expresion_println(p):
    'expresion : PRINTLN PARIZQ expresion PARDER'
    p[0] = Println(p[3])

def p_declaracion_asignacion(p):
    'expresion : tipo ID ASIGNACION expresion'
    p[0] = Asignacion(p[1], p[2], p[4])

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de entrada inesperado")

#comentarios
def p_comentario_multi_linea(t):
    'comentario_multi_linea : COMENTARIO_MULTILINEA'
    comentarios.append(f'Comentario Multilínea: {t[1]}')
    print(f'Comentario Multilínea: {t[1]}')

def p_comentario_una_linea(t):
    'comentario_una_linea : COMENTARIO_UNA_LINEA'
    comentarios.append(f'Comentario de una línea: {t[1]}')
    print(f'Comentario de una línea: {t[1]}')

parser = yacc.yacc(start='inicio')
