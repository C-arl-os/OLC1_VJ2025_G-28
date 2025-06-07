import ply.ply.lex as lex

# Lista de nombres de tokens
tokens = (
    'NUMERO',
    'MAS',
    'MENOS',
    'DECIMAL',
    'BOLEANO',
    'CARACTER',
    'CADENA',
    'ID',
    'ASIGNACION',
    'PTCOMA'
)

# Reglas para tokens de un solo carácter
t_MAS   = r'\+'
t_MENOS = r'-'

t_ASIGNACION = r'='
t_PTCOMA = r';'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'



# manejo de asignacion de variables
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_DECIMAL(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Error al convertir decimal → '{t.value}', se asigna valor 0.0")
        t.value = 0.0
    return t

def t_NUMERO(t):
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

def t_CADENA(t):
    r'"([^\\"]|\\.)*"'
    try:
        # Procesa secuencias de escape como \n, \" usando unicode_escape
        t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
    except Exception as e:
        print(f"Error al procesar cadena: {t.value} → {e}")
        t.value = ""
    return t

def t_CARACTER(t):
    r"\'(\\[ntr'\"\\]|[^\\'])\'"
    try:
        contenido = t.value[1:-1]  # Elimina las comillas simples
        if contenido.startswith("\\"):
            # Decodifica secuencia de escape
            t.value = bytes(contenido, "utf-8").decode("unicode_escape")
        else:
            t.value = contenido
    except Exception as e:
        print(f"Error al procesar carácter: {t.value} → {e}")
        t.value = '\u0000'  # Valor por defecto: carácter nulo
    return t

def t_BOLEANO(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: caracter inesperado '{t.value[0]}'")

lexer = lex.lex()
