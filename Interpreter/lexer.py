import ply.lex as lex

states = (
    ('comentariounico', 'exclusive'),
    ('comentmulti', 'exclusive'),
)

tokens = (
    'NUMERO',
    'MAS',
    'MENOS',
    'C_UNA_LINEA',
    'COMENTARIO',
    'C_MULTI_APERTURA',
    'C_MULTI_CIERRE',
    'COMENTARIO_MULTI'
)

# Reglas para tokens de un solo carácter
t_MAS   = r'\+'
t_MENOS = r'-'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)   #Casteo a int
    return t

def t_C_UNA_LINEA(t):
    r'//'
    t.lexer.begin('comentariounico')
    return t

t_comentariounico_ignore = ' \t'

def t_comentariounico_error(t):
    t.lexer.skip(1)

t_comentmulti_ignore = ' \t'

def t_comentariounico_COMENTARIO(t):
    r'[^\n]+'
    t.lexer.begin('INITIAL')
    return t

def t_C_MULTI_APERTURA(t):
    r'/\*'
    t.lexer.begin('comentmulti')
    return t

def t_comentmulti_COMENTARIO_MULTI(t):
    r'(.|\n)+?(?=\*/)'
    t.value = t.value.strip()
    return t

def t_comentmulti_C_MULTI_CIERRE(t):
    r'\*/'
    t.lexer.begin('INITIAL')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: caracter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

def t_comentmulti_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comentmulti_error(t):
    t.lexer.skip(1)

lexer = lex.lex()