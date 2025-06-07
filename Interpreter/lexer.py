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
    'ID',
    'COMENTARIO_MULTILINEA',
    'COMENTARIO_UNA_LINEA',
) + tuple(reserved.values())
# Tokens

states = (
    ('comentario','exclusive'),
)

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

#def t_comentmulti_newline(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)

#def t_comentmulti_error(t):
#    t.lexer.skip(1)

##### COMENTARIOS


def t_COMENTARIO_INICIO(t):
    r'/\*'
    t.lexer.push_state('comentario')
    t.lexer.comment_value = ''  # Inicializa acumulador
    # No retorna token aquí, el token se retorna cuando termina el comentario

# Estado comentario: salto de línea
def t_comentario_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.comment_value += '\n'

# Estado comentario: contenido dentro del comentario (excepto * y \n)
def t_comentario_content(t):
    r'[^*\n]+|\*+[^/\n]'
    t.lexer.comment_value += t.value

# Estado comentario: fin de comentario */
def t_comentario_end(t):
    r'\*/'
    t.lexer.pop_state()
    t.type = 'COMENTARIO_MULTILINEA'
    t.value = t.lexer.comment_value
    return t

# Ignorar espacios y tab en estado comentario
t_comentario_ignore = ' \t'

# Error en estado comentario
def t_comentario_error(t):
    t.lexer.skip(1)



def t_COMENTARIO_UNA_LINEA(t):
    r'//[^\n]*'
    return t


lexer = lex.lex()