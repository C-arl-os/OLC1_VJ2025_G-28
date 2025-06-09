'''
int x = 1;
x--;
Println(x);
x++;
Println(x);
Println(4<5);
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

Println("Hola");
Println("mundo");
Println(5561);
'''

# Parseamos la entrada
from parser import parser, comentarios
from contexto import tabla_variables,salidas_de_impresion  # Asegúrate de tener esta variable accesible

def analizar_texto(texto):
    salida = []
    comentarios.clear()
    tabla_variables.clear()
    salidas_de_impresion.clear() #

    arboles = []

    raiz = parser.parse(texto)
    if raiz is None:
        return "Error de sintaxis"
    elif isinstance(raiz, list):
        arboles.extend(raiz)
    else:
        arboles.append(raiz)

    # AST
    salida.append("AST:")
    for nodo in arboles:
        salida.append(str(nodo))
        
    

    # Interpretación
    salida.append("\nInterpretación:")
    for nodo in arboles:
        if hasattr(nodo, 'interpret'):
            salida.append(str(nodo.interpret()))

    # Tabla de variables
    salida.append("\nTabla de variables:")
    for var, val in tabla_variables.items():
        salida.append(f"{var} = {val}")

    # Comentarios
    if comentarios:
        salida.append("\nComentarios:")
        salida.extend(comentarios)

    return '\n'.join(salida)



#LEER POR FAVOR
# PARA HACERLO FUNCIONAR
# ESCRIBIR PYTHON APP.PY HUBICADOS EN LA CARPETA "INTERPRETER"