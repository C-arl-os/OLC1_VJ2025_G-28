'''
println("Igual");
int e = 3;
do {
    println(e);
    e = 0;   
} while (e == 3);
int f = 1;
println("Distinto");
do {
    println(f);
    f++;
} while (f != 4);

println("Mayor o igual");
int d = 5;
do {
    Println(d);
    d--;
} while (d >= 3);

println("Mayor que");
int c = 5;
do {
    Println(c);
    c--;
} while (c > 2);

println("Menor o igual");
int b = 1;
do {
    Println(b);
    b++;
} while (b <= 3);

println("Menor que");
int a = 1;
do {
    println(a);
    a++;
} while (a < 4);

int x = 1;
int y = 5;
do {
    println(x);
    x++;
while (y >= 3) {
    println("");
    println(y);
    y--;
}

} while (x <= 3);

int x = 1;
while (x <= 3) {
    Println(x);
    x++;
}
println("");
int y = 5;
while (y >= 3) {
    Println(y);
    y--;
}
println("");
int z = 0;
while (z == 0) {
    Println(z);
    z = 1;
}
println("");
int w = 2;
while (w != 0) {
    Println(w);
    w--;
}
int x = 1;
x--;
println(x);
x++;
println(x);
println(4<5);
int s1 = 5 + 5;
float s2 = 5 + 2.5;
int s3 = 5 + 'A';
string s4 = 5 + "texto";
float s5 = 2.5 + 'A';
string s6 = "hola" + 10;
string s7 = "cadena" + 'B';
string s8 = 'A' + 'B';
string s9 = true + " verdad";
int s10 = 'A' + 1;

int r1 = 10 - 2;
float r2 = 10 - 2.5;
int r3 = 65 - 'A';
float r4 = 2.5 - 1;
float r5 = 5.5 - 1.5;
float r6 = 5.5 - 'A';
int r7 = 'B' - 1;
float r8 = 'C' - 2.5;
int r9 = 'X' - 'Y'; 

int m1 = 2 * 3;
float m2 = 2 * 3.5;
int m3 = 2 * 'A';
float m4 = 2.5 * 2;
float m5 = 2.5 * 3.5;
float m6 = 2.5 * 'A';
int m7 = 'B' * 2;
float m8 = 'C' * 2.5;
int m9 = 'A' * 'B';  

float d1 = 5 / 2;
float d2 = 5 / 2.0;
float d3 = 66 / 'B';
float d4 = 5.0 / 2;
float d5 = 5.5 / 2.2;
float d6 = 162.5 / 'A';
float d7 = 'D' / 2;
float d8 = 'C' / 2.0;
float d9 = 'Z' / 'Z';

int p1 = 2 ** 3;
float p2 = 2 ** 3.0;
float p3 = 2.5 ** 2;
float p4 = 2.5 ** 3;

float md1 = 10 % 3;
float md2 = 10 % 3.5;
float md3 = 5.5 % 2;
float md4 = 5.5 % 2.2;

int a = -5;
float b = -3.14;
int c = -a;
float d = -b;

println("Hola");
println("mundo");
println(5561);
'''

# Parseamos la entrada
from parser import parser, comentarios, errores_sintacticos
from contexto import tabla_variables, salidas_de_impresion
from lexer import lexer, errores_lexicos, graficar_tabla_tokens, graficar_tabla_errores

def analizar_texto(texto):
    errores_semanticos = []
    salida = []

    # Limpiar estados de ejecuciones previas
    errores_lexicos.clear()
    errores_sintacticos.clear()
    salidas_de_impresion.clear()
    tabla_variables.clear()

    # === Generar archivo HTML con tokens ===
    graficar_tabla_tokens(texto)

    # === Tabla de Tokens ===
    lexer.input(texto)
    while True:
        tok = lexer.token()
        if not tok:
            break
        columna = encontrar_columna(texto, tok.lexpos)
        salida.append(f"{tok.value}\t\t{tok.type}\t\t{tok.lineno}\t{columna}")

    # ——— Limpiar errores léxicos de las fases anteriores ———
    errores_lexicos.clear()
        
    

    # === Parseo y construcción de lista de AST ===
    arboles = []
    raiz = parser.parse(texto)
    if raiz is None:
        salida.append("\nError de sintaxis: No se pudo generar el árbol.")
        return "\n".join(salida)
    arboles = raiz if isinstance(raiz, list) else [raiz]

    # === AST ===
    salida.append("\nAST:")
    for nodo in arboles:
        salida.append(str(nodo))

    # === Interpretación + Errores Semánticos ===
    for nodo in arboles:
        try:
            nodo.interpret()
        except Exception as e:
            errores_semanticos.append({
                'tipo': 'Semántico',
                'descripcion': str(e),
                'linea': getattr(nodo, 'linea', -1),
                'columna': getattr(nodo, 'columna', -1)
            })

    # === Salidas de Println ===
    if salidas_de_impresion:
        salida.append("\nSalida de Println:")
        salida.extend(salidas_de_impresion)

    # === Tabla de Variables ===
    salida.append("\nTabla de variables:")
    for var, val in tabla_variables.items():
        salida.append(f"{var} = {val}")

    # === Tabla de Errores ===
    salida.append("\nTabla de errores:")
    salida.append("Tipo\tDescripción\tLínea\tColumna")
    for tbl in errores_lexicos + errores_sintacticos + errores_semanticos:
        salida.append(f"{tbl['tipo']}\t{tbl['descripcion']}\t{tbl['linea']}\t{tbl['columna']}")

    #Graficar tabla de errores
    # Crear tabla HTML de errores (DEBE SER DESPUÉS de llenar las listas de errores)
    # Al final de analizar_texto, antes del return:
    graficar_tabla_errores(errores_lexicos, errores_sintacticos, errores_semanticos)

    return "\n".join(salida)

def encontrar_columna(input_text, lexpos):
    """Calcula la columna a partir del lexpos."""
    last_newline = input_text.rfind('\n', 0, lexpos)
    if last_newline < 0:
        return lexpos + 1
    else:
        return lexpos - last_newline

