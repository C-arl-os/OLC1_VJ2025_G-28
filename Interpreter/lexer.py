import ply.lex as lex
reserved = {
    'int': 'INT',
}

<<<<<<< HEAD
# Lista de nombres de tokens
tokens  = (
    
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ENTERO',
    'PTCOMA',
    'FLOTANTE',
    'IGUAL',
    'ID'
) + tuple(reserved.values())
# Tokens
=======
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
>>>>>>> Operaciones

t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_PTCOMA    = r';'
t_IGUAL = r'='
# Ignorar espacios y tabulaciones
t_ignore = ' \t'
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Si es "int", clasifícalo como palabra reservada
    return t

<<<<<<< HEAD
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


=======
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
>>>>>>> Operaciones

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