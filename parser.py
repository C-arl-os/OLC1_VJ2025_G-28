import ply.yacc as yacc
from lexer import tokens, lexer  # Importar tokens y lexer

# Reglas gramaticales

def p_instrucciones(t):
    '''instrucciones : instruccion instrucciones
                     | instruccion'''
    pass

def p_instruccion(t):
    '''instruccion : comentario_una_linea
                   | comentario_multi_linea'''
    pass

def p_comentario_una_linea(t):
    'comentario_una_linea : CUNALINEA COMENTARIO'
    print(f'Apertura Comentario Unico : {t[1]}')
    print(f'Comentario: {t[2]}')

def p_comentario_multi_linea(t):
    'comentario_multi_linea : CMULTILINEAAPERTURA COMENTARIOMULTI CMULTILINEACIERRE'
    print(f'Apertura Comentario: {t[1]}')
    print(f'Comentario: {t[2]}')
    print(f'Cierre Comentario: {t[3]}')

# Declaramos el símbolo inicial
start = 'instrucciones'

# Construcción del parser
parser = yacc.yacc()
