import ply.lex as lex

# Definición de estados para comentarios
states = (
    ('comentariounico', 'exclusive'),
    ('comentmulti', 'exclusive'),
)

# Lista de tokens
tokens = (
    'INT', 'STR', 'DBL', 'BOOL', 'ID', 'IGUAL', 'ENTERO', 'TEXTO',
    'DECIMAL', 'BOOLEANO', 'CUNALINEA', 'CMULTILINEAAPERTURA',
    'CMULTILINEACIERRE', 'COMENTARIO', 'COMENTARIOMULTI', 'PTCOMA'
)

# Tokens simples
t_INT      = r'int'
t_STR      = r'string'
t_DBL      = r'double'
t_BOOL     = r'boolean'
t_IGUAL    = r'='
t_PTCOMA   = r';'

# Tokens con acciones especiales
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_ENTERO(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_TEXTO(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CUNALINEA(t):
    r'//'
    t.lexer.begin('comentariounico')
    return t

def t_comentariounico_COMENTARIO(t):
    r'[^\n]+'
    t.lexer.begin('INITIAL')
    return t

def t_CMULTILINEAAPERTURA(t):
    r'/\*'
    t.lexer.begin('comentmulti')
    return t

def t_comentmulti_COMENTARIOMULTI(t):
    r'(.|\n)+?(?=\*/)'
    t.value = t.value.strip()
    return t

def t_comentmulti_CMULTILINEACIERRE(t):
    r'\*/'
    t.lexer.begin('INITIAL')
    return t

def t_comentmulti_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comentmulti_error(t):
    t.lexer.skip(1)

def t_BOOLEANO(t):
    r'(true|false)'
    t.value = True if t.value == 'true' else False
    return t

# Ignorar espacios y tabs
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()
