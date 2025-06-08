import ply.ply.lex as lex

# palabras reservadas
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'BOLEANO',
    'false': 'BOLEANO',
}

# Lista de nombres de tokens
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'DECIMAL',
    'ENTERO',
    'CARACTER',
    'CADENA',
    'ID',
    'ASIGNACION',
    'PTCOMA',
    'POR',
    'DIVIDIDO',
    'POTENCIA',
    'MODULO',
    'COMENTARIO_MULTILINEA',
    'COMENTARIO_UNA_LINEA',
) + tuple(reserved.values())
# Tokens

states = (
    ('comentario','exclusive'),
)

t_PARIZQ    = r'\('
t_PARDER    = r'\)'
# Reglas para tokens de un solo carácter
t_MAS   = r'\+'
t_MENOS = r'-'
t_ASIGNACION = r'='
t_PTCOMA = r';'
t_POTENCIA = r'\*\*'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MODULO = r'%'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_DECIMAL(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Error al convertir decimal → '{t.value}', se asigna valor 0.0")
        t.value = 0.0
    return t

def t_ENTERO(t):
    r'-?\d+'
    try:
        valor = int(t.value)
        if -2147483648 <= valor <= 2147483647:
            t.value = valor
        else:
            print(f"Advertencia: número fuera de rango int32 → '{t.value}', se asigna valor 0")
            t.value = 0
    except ValueError:
        print(f"Error al convertir número → '{t.value}', se asigna valor 0")
        t.value = 0
    return t

def t_BOLEANO(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


def t_CARACTER(t):
    r"\'(\\[ntr'\"\\]|[^\\'])\'"
    try:
        contenido = t.value[1:-1]  
        if contenido.startswith("\\"):
            t.value = bytes(contenido, "utf-8").decode("unicode_escape")
        else:
            t.value = contenido
    except Exception as e:
        print(f"Error al procesar carácter: {t.value} → {e}")
        t.value = '\u0000'  # Valor por defecto: carácter nulo
    return t

def t_CADENA(t):
    r'"([^\\"]|\\.)*"'
    try:
        t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
    except Exception as e:
        print(f"Error al procesar cadena: {t.value} → {e}")
        t.value = ""
    return t

# manejo de asignacion de variables
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
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