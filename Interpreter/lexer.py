import ply.lex as lex
from graphviz import Digraph
import os
# palabras reservadas
reserved = {
    'eval':'REVAL',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'println': 'PRINTLN',
    'while':'WHILE',
    'if':'IF',
    'else':'ELSE',
    'for':'FOR',
    'do':'DO',
    'break': 'BREAK',
    'continue': 'CONTINUE', 
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'vector': 'VECTOR',  # Nuevo token para Vector
    'seno': 'SENO',
    'coseno': 'COSENO',
    'inv': 'INV',
    'proc': 'PROC',
    'exec': 'EXEC',
    'shuffle' : 'SHUFFLE',
    'sort' : 'SORT'
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
    'GE',  # >=
    'LE',  # <=
    'LT',  # <
    'GT',  # >
    'EQ',  # ==
    'NE', # !=
    'INCREMENTO',  # ++
    'DECREMENTO',  # --
    'LLAVE_IZQ',  # {
    'LLAVE_DER',  # }
    'CORDER',  # [ ciclo while
    'CORIZQ',  # ] ciclo while
    'IGUAL', #igual
    'MAYORQ', #>
    'PTC',
    'OR_LOGICO',  # ||
    'AND_LOGICO',  # &&
    'NOT_LOGICO',  # !
    'XOR_LOGICO',  # ^
    'DO',
    'DOSPUNTOS',
    'COMENTARIO_MALFORMADO',
    'COMA'  # Nueva coma para separar elementos
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
# Reglas para operadores lógicos
t_OR_LOGICO = r'\|\|'
t_AND_LOGICO = r'&&'
t_NOT_LOGICO = r'!'
t_XOR_LOGICO = r'\^'
# Reglas para los operadores de comparación
t_GE = r'>='
t_LE = r'<='
t_LT = r'<'
t_GT = r'>'
t_EQ = r'=='
t_NE     = r'!='   # <- Nuevo
# Reglas para los operadores de incremento y decremento
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
# Ignorar espacios y tabulaciones
t_ignore = ' \t\r'
#ciclo while
t_CORIZQ = r'\['  # Cambiar orden
t_CORDER = r'\]'
t_IGUAL = r'='
t_MAYORQ = r'>'
t_PTC = r';'
t_DOSPUNTOS = r':'
#matriz 
t_COMA = r','
# lista global de errores
errores_lexicos = []

errores_sintacticos = []

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


def t_CARACTER(t):
    r"\'(\\[ntr'\"\\]|[^\\'])\'"
    try:
        contenido = t.value[1:-1]  
        if contenido.startswith("\\"):
            t.value = bytes(contenido, "utf-8").decode("unicode_escape")
        else:
            t.value = contenido
        # print(f"Token CARACTER capturado: {repr(t.value)}")
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
    r'[a-zA-Z][a-zA-Z0-9_]*'
    palabra = t.value
    t.type = reserved.get(palabra.lower(), 'ID')
    # Solo cambia a minúsculas palabra reservada
    if t.type in reserved.values():
        t.value = palabra.lower()
    else:
        t.value = palabra  # Mantén el valor original
    return t
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_COMENTARIO_MALFORMADO(t):
    r'/[^*/\s][^\n\s]*'  # '/' seguido de texto que no sea '*' o '/' o espacios
    data = t.lexer.lexdata
    col = data.rfind('\n', 0, t.lexpos)
    col = t.lexpos - col
    
    errores_lexicos.append({
        'tipo': 'Léxico',
        'descripcion': f"Comentario malformado: '{t.value}'",
        'linea': t.lineno,
        'columna': col
    })
    # No retornar token, solo registrar el error y continuar
    pass

def t_error(t):
    # calculamos columna desde t.lexpos y t.lexer.lexdata
    data = t.lexer.lexdata
    col = data.rfind('\n', 0, t.lexpos)
    col = t.lexpos - col
    
    # Filtrar caracteres no ASCII problemáticos
    char = t.value[0]
    if ord(char) == 0xa0:  # Espacio no-ASCII
        t.lexer.skip(1)
        return
    
    errores_lexicos.append({
        'tipo': 'Léxico',
        'descripcion': f"Caracter inesperado {char!r}",
        'linea': t.lineno,
        'columna': col
    })
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

# Estado comentario: salto de línea
def t_comentario_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.comment_value += '\n'

# Estado comentario: contenido dentro del comentario (excepto * y \n)
def t_comentario_content(t):
    r'[^*\n]+|\*+[^/\n]'
    t.lexer.comment_value += t.value
    pass

# Estado comentario: fin de comentario */
def t_comentario_end(t):
    r'\*/'
    t.lexer.pop_state()
    t.type = 'COMENTARIO_MULTILINEA'
    t.value = t.lexer.comment_value
    #return t

# Ignorar espacios y tab en estado comentario
t_comentario_ignore = ' \t'

# Error en estado comentario
def t_comentario_error(t):
    t.lexer.skip(1)

def t_COMENTARIO_UNA_LINEA(t):
    r'//[^\n]*'
    #return t

def t_PRINTLN(t):
    r'println'
    return t

def generar_tabla_tokens(codigo_fuente):
    lexer.input(codigo_fuente)
    tabla = []
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        fila = {
            'Lexema': tok.value,
            'Token': tok.type,
            'Línea': tok.lineno,
            'Columna': calcular_columna(tok.lexpos, codigo_fuente)
        }
        tabla.append(fila)
    
    return tabla

def graficar_tabla_tokens(codigo_fuente):
    lexer.input(codigo_fuente)
    
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='es'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Tabla de Tokens</title>")
    html.append("<style>")
    html.append("""
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }
    h2 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
        font-size: 28px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
        overflow-x: auto;
    }
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    th {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
        position: sticky;
        top: 0;
    }
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    tr:hover {
        background-color: #f1f7fd;
        transform: scale(1.01);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    td {
        color: #34495e;
    }
    .token-type {
        font-weight: 500;
        color: #e74c3c;
    }
    @media (max-width: 768px) {
        table {
            border-radius: 5px;
        }
        th, td {
            padding: 8px 10px;
        }
    }
    """)
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='container'>")
    html.append("<h2>Tabla de Tokens</h2>")
    html.append("<table>")
    html.append("<thead><tr><th>Lexema</th><th>Token</th><th>Línea</th><th>Columna</th></tr></thead>")
    html.append("<tbody>")

    while True:
        tok = lexer.token()
        if not tok:
            break
        columna = calcular_columna(tok.lexpos, codigo_fuente)
        html.append(f"<tr><td>{tok.value}</td><td class='token-type'>{tok.type}</td><td>{tok.lineno}</td><td>{columna}</td></tr>")

    html.append("</tbody></table>")
    html.append("</div>")
    html.append("</body>")
    html.append("</html>")
  # Crear el directorio Reportes si no existe
    os.makedirs("../Reportes", exist_ok=True)
    # Guardar el HTML en un archivo
    with open("../Reportes/Tabla_de_Tokens.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html))

def graficar_tabla_variables(tabla_variables):
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='es'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Tabla de Variables</title>")
    html.append("<style>")
    html.append("""
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }
    h2 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
        font-size: 28px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .container {
        max-width: 700px;
        margin: 0 auto;
        overflow-x: auto;
    }
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    th {
        background: linear-gradient(135deg, #27ae60, #16a085);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
        position: sticky;
        top: 0;
    }
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    tr:hover {
        background-color: #eafaf1;
        transform: scale(1.01);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    td {
        color: #34495e;
    }
    @media (max-width: 768px) {
        table {
            border-radius: 5px;
        }
        th, td {
            padding: 8px 10px;
        }
    }
    """)
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='container'>")
    html.append("<h2>Tabla de Variables</h2>")
    html.append("<table>")
    html.append("<thead><tr><th>Variable</th><th>Valor</th></tr></thead>")
    html.append("<tbody>")

    for var, val in tabla_variables.items():
        html.append(f"<tr><td>{var}</td><td>{val}</td></tr>")

    html.append("</tbody></table>")
    html.append("</div>")
    html.append("</body>")
    html.append("</html>")

    os.makedirs("../Reportes", exist_ok=True)
    with open("../Reportes/Tabla_de_Variables.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html))

def graficar_tabla_errores(errores_lexicos, errores_sintacticos, errores_semanticos):
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='es'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Tabla de Errores</title>")
    html.append("<style>")
    html.append("""
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }
    h2 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
        font-size: 28px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
        overflow-x: auto;
    }
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    th {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
        position: sticky;
        top: 0;
    }
    tr:nth-child(even) {
        background-color: #fef5f5;
    }
    tr:hover {
        background-color: #ffebee;
        transform: scale(1.01);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .lexico {
        border-left: 4px solid #3498db;
    }
    .sintactico {
        border-left: 4px solid #f39c12;
    }
    .semantico {
        border-left: 4px solid #e74c3c;
    }
    .tipo-error {
        font-weight: 600;
    }
    .lexico .tipo-error {
        color: #3498db;
    }
    .sintactico .tipo-error {
        color: #f39c12;
    }
    .semantico .tipo-error {
        color: #e74c3c;
    }
    @media (max-width: 768px) {
        table {
            border-radius: 5px;
        }
        th, td {
            padding: 8px 10px;
        }
    }
    """)
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='container'>")
    html.append("<h2>Tabla de Errores</h2>")
    html.append("<table>")
    html.append("<thead><tr><th>Tipo</th><th>Descripción</th><th>Línea</th><th>Columna</th></tr></thead>")
    html.append("<tbody>")

    todos_los_errores = errores_lexicos + errores_sintacticos + errores_semanticos
    for error in todos_los_errores:
        tipo_clase = ""
        if error['tipo'].lower() == 'léxico' or error['tipo'].lower() == 'lexico':
            tipo_clase = "lexico"
        elif error['tipo'].lower() == 'sintáctico' or error['tipo'].lower() == 'sintactico':
            tipo_clase = "sintactico"
        elif error['tipo'].lower() == 'semántico' or error['tipo'].lower() == 'semantico':
            tipo_clase = "semantico"
        
        html.append(f"""
        <tr class="{tipo_clase}">
            <td class="tipo-error">{error['tipo']}</td>
            <td>{error['descripcion']}</td>
            <td>{error['linea']}</td>
            <td>{error['columna']}</td>
        </tr>
        """)

    html.append("</tbody></table>")
    html.append("</div>")
    html.append("</body>")
    html.append("</html>")

    with open("../Reportes/Tabla_de_Errores.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html))

def graficar_tabla_advertencias(advertencias):
    """Genera un reporte HTML de advertencias"""
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='es'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Tabla de Advertencias</title>")
    html.append("<style>")
    html.append("""
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }
    h2 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
        font-size: 28px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
        overflow-x: auto;
    }
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    th {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
        position: sticky;
        top: 0;
    }
    tr:nth-child(even) {
        background-color: #fff9e6;
    }
    tr:hover {
        background-color: #fffbee;
        transform: scale(1.01);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .warning-icon {
        color: #f39c12;
        font-weight: bold;
        margin-right: 5px;
    }
    .no-warnings {
        text-align: center;
        padding: 40px;
        color: #27ae60;
        font-size: 18px;
        font-weight: 500;
    }
    """)
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='container'>")
    html.append("<h2>⚠️ Tabla de Advertencias</h2>")
    
    if not advertencias:
        html.append("<div class='no-warnings'>")
        html.append("✅ No se encontraron advertencias en el código")
        html.append("</div>")
    else:
        html.append("<table>")
        html.append("<thead>")
        html.append("<tr>")
        html.append("<th>Tipo</th>")
        html.append("<th>Descripción</th>")
        html.append("<th>Línea</th>")
        html.append("<th>Columna</th>")
        html.append("</tr>")
        html.append("</thead>")
        html.append("<tbody>")
        
        for adv in advertencias:
            html.append("<tr>")
            html.append(f"<td><span class='warning-icon'>⚠️</span>{adv['tipo']}</td>")
            html.append(f"<td>{adv['descripcion']}</td>")
            html.append(f"<td>{adv['linea']}</td>")
            html.append(f"<td>{adv['columna']}</td>")
            html.append("</tr>")
        
        html.append("</tbody>")
        html.append("</table>")
    
    html.append("</div>")
    html.append("</body>")
    html.append("</html>")
    
    # Crear directorio si no existe
    reportes_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Reportes')
    os.makedirs(reportes_dir, exist_ok=True)
    
    # Escribir archivo HTML
    with open(os.path.join(reportes_dir, 'Tabla_de_Advertencias.html'), 'w', encoding='utf-8') as f:
        f.write("\n".join(html))

def graficar_ast(arboles, output_path_pdf='Reportes/AST'):
    dot = Digraph(comment='Árbol de Sintaxis Abstracta')
    dot.attr(rankdir='TB')

    contador = {'n': 0}

    def agregar_nodo(dot, nodo, padre_id=None):
        nodo_id = f"n{contador['n']}"
        contador['n'] += 1

        label = nodo.__class__.__name__
        if hasattr(nodo, 'valor'):
            label += f"\\n{nodo.valor}"
        elif hasattr(nodo, 'nombre'):
            label += f"\\n{nodo.nombre}"
        elif hasattr(nodo, 'contenido'):
            label += f"\\n{nodo.contenido}"

        dot.node(nodo_id, label)

        if padre_id:
            dot.edge(padre_id, nodo_id)

        if hasattr(nodo, 'hijos'):
            for hijo in nodo.hijos:
                if hijo:
                    agregar_nodo(dot, hijo, nodo_id)
        elif hasattr(nodo, '__dict__'):
            for attr in nodo.__dict__.values():
                if isinstance(attr, list):
                    for item in attr:
                        if hasattr(item, '__class__'):
                            agregar_nodo(dot, item, nodo_id)
                elif hasattr(attr, '__class__'):
                    agregar_nodo(dot, attr, nodo_id)

    for raiz in arboles:
        agregar_nodo(dot, raiz)

    # Asegura la carpeta destino
    os.makedirs(os.path.dirname(output_path_pdf), exist_ok=True)

    # === Guardar como PDF ===
    dot.render(output_path_pdf, format='pdf', cleanup=True)
    
def calcular_columna(lexpos, texto):
    # Calcula la columna a partir del lexpos
    ultima_linea = texto.rfind('\n', 0, lexpos)
    if ultima_linea < 0:
        ultima_linea = -1
    return lexpos - ultima_linea

lexer = lex.lex()

def graficar_tabla_variables_detallada(tabla_variables):
    """Genera un reporte HTML detallado de la tabla de variables con estilo moderno"""
    html_content = """
    <!DOCTYPE html>
    <html lang='es'>
    <head>
        <meta charset='UTF-8'>
        <title>Reporte Detallado de Variables</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 25px;
                font-size: 28px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                overflow-x: auto;
            }
            table {
                border-collapse: separate;
                border-spacing: 0;
                width: 100%;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            th, td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #e0e0e0;
            }
            th {
                background: linear-gradient(135deg, #27ae60, #16a085);
                color: white;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 14px;
                letter-spacing: 0.5px;
                position: sticky;
                top: 0;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            tr:hover {
                background-color: #eafaf1;
                transform: scale(1.01);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .variable-name {
                font-weight: bold;
                color: #e74c3c;
                font-size: 16px;
            }
            .data-type {
                color: #27ae60;
                font-weight: 500;
                font-style: italic;
            }
            .vector-structure {
                font-family: 'Courier New', monospace;
                white-space: pre-wrap;
                background-color: #f4f4f4;
                padding: 8px;
                border-radius: 4px;
                border-left: 3px solid #3498db;
                max-width: 400px;
                overflow-x: auto;
            }
            .simple-value {
                color: #34495e;
                font-weight: 500;
            }
            .vector-badge {
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }
            .simple-badge {
                background: linear-gradient(135deg, #95a5a6, #7f8c8d);
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }
            .dimensions {
                color: #8e44ad;
                font-weight: bold;
            }
            .no-variables {
                text-align: center;
                padding: 40px;
                color: #7f8c8d;
                font-size: 18px;
                font-weight: 500;
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin-bottom: 20px;
                gap: 10px;
            }
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                flex: 1;
            }
            .stat-number {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            .stat-label {
                color: #7f8c8d;
                margin-top: 5px;
            }
            @media (max-width: 768px) {
                table {
                    border-radius: 5px;
                }
                th, td {
                    padding: 8px 10px;
                }
                .stats {
                    flex-direction: column;
                }
                .vector-structure {
                    max-width: 200px;
                }
            }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>📊 Reporte Detallado de Variables</h1>
    """
    
    def format_vector_data(data, dimensiones, nivel=0):
        """Formatea recursivamente los datos del vector para mostrar su estructura"""
        indent = "  " * nivel
        if nivel == len(dimensiones) - 1:
            # Último nivel, mostrar los valores
            return f"{indent}[{', '.join(map(str, data))}]"
        else:
            # Niveles intermedios
            result = f"{indent}[\n"
            for i, sub_data in enumerate(data):
                result += format_vector_data(sub_data, dimensiones, nivel + 1)
                if i < len(data) - 1:
                    result += ",\n"
                else:
                    result += "\n"
            result += f"{indent}]"
            return result
    
    # Estadísticas
    total_variables = len(tabla_variables)
    variables_simples = 0
    variables_vectores = 0
    
    for var_value in tabla_variables.values():
        if isinstance(var_value, dict) and var_value.get('tipo') == 'vector':
            variables_vectores += 1
        else:
            variables_simples += 1
    
    # Agregar estadísticas
    html_content += f"""
            <div class='stats'>
                <div class='stat-card'>
                    <div class='stat-number'>{total_variables}</div>
                    <div class='stat-label'>Total Variables</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-number'>{variables_simples}</div>
                    <div class='stat-label'>Variables Simples</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-number'>{variables_vectores}</div>
                    <div class='stat-label'>Vectores</div>
                </div>
            </div>
    """
    
    if not tabla_variables:
        html_content += """
            <div class='no-variables'>
                📝 No se han declarado variables en el programa
            </div>
        """
    else:
        html_content += """
            <table>
                <thead>
                    <tr>
                        <th>🏷️ Variable</th>
                        <th>🏗️ Tipo</th>
                        <th>🔧 Subtipo</th>
                        <th>📏 Dimensiones</th>
                        <th>💾 Estructura de Datos</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for var_name, var_value in tabla_variables.items():
            if isinstance(var_value, dict) and var_value.get('tipo') == 'vector':
                # Es un vector
                tipo = var_value.get('tipo', 'N/A')
                subtipo = var_value.get('subtipo', 'N/A')
                dimensiones = var_value.get('dimensiones', [])
                data = var_value.get('data', [])
                
                dimensiones_str = ' × '.join(map(str, dimensiones))
                estructura_data = format_vector_data(data, dimensiones)
                
                html_content += f"""
                    <tr>
                        <td class="variable-name">{var_name}</td>
                        <td><span class="vector-badge">{tipo.upper()}</span></td>
                        <td class="data-type">{subtipo}</td>
                        <td class="dimensions">{dimensiones_str}</td>
                        <td class="vector-structure">{estructura_data}</td>
                    </tr>
                """
            else:
                # Variable simple
                tipo = type(var_value).__name__
                valor_mostrar = str(var_value)
                if isinstance(var_value, str):
                    valor_mostrar = f'"{var_value}"'
                elif isinstance(var_value, bool):
                    valor_mostrar = str(var_value).lower()
                
                html_content += f"""
                    <tr>
                        <td class="variable-name">{var_name}</td>
                        <td><span class="simple-badge">{tipo.upper()}</span></td>
                        <td>-</td>
                        <td>-</td>
                        <td class="simple-value">{valor_mostrar}</td>
                    </tr>
                """
        
        html_content += """
                </tbody>
            </table>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    try:
        os.makedirs("../Reportes", exist_ok=True)
        with open('../Reportes/tabla_variables_detallada.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        print("Reporte detallado de tabla de variables generado: Reportes/tabla_variables_detallada.html")
    except Exception as e:
        print(f"Error al generar el reporte detallado de tabla de variables: {e}")