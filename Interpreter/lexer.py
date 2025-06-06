import ply.lex as lex
reserved = {
    'int': 'INT',
}

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

def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: caracter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
