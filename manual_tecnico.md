# Manual Técnico - Intérprete OLC1_VJ2025_G-28

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Gramática en BNF](#gramática-en-bnf)
4. [Análisis Léxico](#análisis-léxico)
5. [Análisis Sintáctico](#análisis-sintáctico)
6. [Análisis Semántico](#análisis-semántico)
7. [Estructuras de Datos](#estructuras-de-datos)
8. [Manejo de Errores](#manejo-de-errores)
9. [Generación de Reportes](#generación-de-reportes)

## Introducción

Este manual técnico describe la implementación de un intérprete desarrollado en Python utilizando PLY (Python Lex-Yacc) para el curso de Organización de Lenguajes y Compiladores 1. El intérprete soporta múltiples tipos de datos, estructuras de control, vectores multidimensionales y procedimientos.

## Arquitectura del Sistema

### Componentes Principales

- **Lexer (`lexer.py`)**: Análisis léxico y tokenización
- **Parser (`parser.py`)**: Análisis sintáctico y construcción del AST
- **AST Nodes (`ast_nodes.py`)**: Nodos del árbol de sintaxis abstracta
- **Context (`contexto.py`)**: Manejo de contexto y variables
- **Symbol Table**: Tabla de símbolos para variables y procedimientos
- **App (`app.py`)**: Interfaz web con Flask

### Tecnologías Utilizadas

- **Python 3.x**
- **PLY (Python Lex-Yacc)**: Para análisis léxico y sintáctico
- **Flask**: Para la interfaz web
- **Graphviz**: Para generación de diagramas AST

## Gramática en BNF

### Símbolos Terminales

```bnf
PARIZQ := '('
PARDER := ')'
MAS := '+'
MENOS := '-'
POR := '*'
DIVIDIDO := '/'
POTENCIA := '**'
MODULO := '%'
ASIGNACION := '='
PTCOMA := ';'
LLAVE_IZQ := '{'
LLAVE_DER := '}'
CORIZQ := '['
CORDER := ']'
COMA := ','
DOSPUNTOS := ':'
GE := '>='
LE := '<='
LT := '<'
GT := '>'
EQ := '=='
NE := '!='
OR_LOGICO := '||'
AND_LOGICO := '&&'
NOT_LOGICO := '!'
XOR_LOGICO := '^'
INCREMENTO := '++'
DECREMENTO := '--'
```

### Gramática Principal

```bnf
<inicio> ::= <lista_expresiones>
          | <expresion>
          | <comentario_una_linea>
          | <comentario_multi_linea>

<lista_expresiones> ::= <expresion> PTCOMA
                     | <expresion>
                     | <lista_expresiones> <expresion> PTCOMA
                     | <lista_expresiones> <expresion>

<expresion> ::= <expresion_aritmetica>
             | <expresion_relacional>
             | <expresion_logica>
             | <expresion_control>
             | <expresion_vector>
             | <expresion_procedimiento>
             | <declaracion>
             | <asignacion>
             | <println>
             | <literal>
             | ID
```

### Expresiones Aritméticas

```bnf
<expresion_aritmetica> ::= <expresion> MAS <expresion>
                        | <expresion> MENOS <expresion>
                        | <expresion> POR <expresion>
                        | <expresion> DIVIDIDO <expresion>
                        | <expresion> POTENCIA <expresion>
                        | <expresion> MODULO <expresion>
                        | MENOS <expresion> %prec UMINUS
                        | SENO PARIZQ <expresion> PARDER
                        | COSENO PARIZQ <expresion> PARDER
                        | INV PARIZQ <expresion> PARDER
                        | PARIZQ <expresion> PARDER
```

### Expresiones Relacionales

```bnf
<expresion_relacional> ::= <expresion> GE <expresion>
                        | <expresion> LE <expresion>
                        | <expresion> LT <expresion>
                        | <expresion> GT <expresion>
                        | <expresion> EQ <expresion>
                        | <expresion> NE <expresion>
```

### Expresiones Lógicas

```bnf
<expresion_logica> ::= <expresion> OR_LOGICO <expresion>
                    | <expresion> AND_LOGICO <expresion>
                    | NOT_LOGICO <expresion>
                    | <expresion> XOR_LOGICO <expresion>
```

### Estructuras de Control

```bnf
<expresion_control> ::= <if_stmt>
                     | <while_stmt>
                     | <do_while_stmt>
                     | <for_stmt>
                     | <switch_stmt>
                     | <break_stmt>
                     | <continue_stmt>

<if_stmt> ::= IF PARIZQ <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER
           | IF PARIZQ <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER ELSE LLAVE_IZQ <lista_expresiones> LLAVE_DER
           | IF PARIZQ <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER ELSE <expresion>
           | IF PARIZQ <expresion> PARDER LLAVE_IZQ LLAVE_DER

<while_stmt> ::= WHILE PARIZQ <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER
              | WHILE PARIZQ <expresion> PARDER LLAVE_IZQ LLAVE_DER

<do_while_stmt> ::= DO LLAVE_IZQ <lista_expresiones> LLAVE_DER WHILE PARIZQ <expresion> PARDER PTCOMA
                 | DO LLAVE_IZQ LLAVE_DER WHILE PARIZQ <expresion> PARDER PTCOMA

<for_stmt> ::= FOR PARIZQ <tipo> ID ASIGNACION <expresion> PTCOMA <expresion> PTCOMA <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER
            | FOR PARIZQ ID ASIGNACION <expresion> PTCOMA <expresion> PTCOMA <expresion> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER
            | FOR PARIZQ <tipo> ID ASIGNACION <expresion> PTCOMA <expresion> PTCOMA <expresion> PARDER LLAVE_IZQ LLAVE_DER
            | FOR PARIZQ ID ASIGNACION <expresion> PTCOMA <expresion> PTCOMA <expresion> PARDER LLAVE_IZQ LLAVE_DER

<switch_stmt> ::= SWITCH PARIZQ <expresion> PARDER LLAVE_IZQ <lista_cases_opt> LLAVE_DER

<lista_cases_opt> ::= <lista_cases> <case_default>
                   | <lista_cases>

<lista_cases> ::= <lista_cases> <case>
               | <case>

<case> ::= CASE <expresion> DOSPUNTOS <lista_expresiones>

<case_default> ::= DEFAULT DOSPUNTOS <lista_expresiones>

<break_stmt> ::= BREAK PTCOMA

<continue_stmt> ::= CONTINUE PTCOMA
```

### Vectores

```bnf
<expresion_vector> ::= <vector_declaracion>
                    | <vector_acceso>
                    | <vector_asignacion>
                    | <vector_inicializacion>

<vector_declaracion> ::= VECTOR CORIZQ <tipo> CORDER ID PARIZQ <lista_dimensiones> PARDER PTCOMA
                      | VECTOR CORIZQ <tipo> CORDER ID PARIZQ ENTERO PARDER PTCOMA

<vector_inicializacion> ::= VECTOR CORIZQ <tipo> CORDER ID PARIZQ <lista_dimensiones> PARDER ASIGNACION <lista_valores> PTCOMA
                         | VECTOR CORIZQ <tipo> CORDER ID PARIZQ ENTERO PARDER ASIGNACION CORIZQ <lista_elementos> CORDER PTCOMA
                         | VECTOR CORIZQ <tipo> CORDER ID PARIZQ <lista_dimensiones> PARDER ASIGNACION <estructura_multidimensional> PTCOMA
                         | VECTOR CORIZQ <tipo> CORDER ID PARIZQ <lista_dimensiones> PARDER ASIGNACION SHUFFLE PARIZQ ID PARDER PTCOMA
                         | VECTOR CORIZQ <tipo> CORDER ID PARIZQ ENTERO PARDER ASIGNACION SORT PARIZQ ID PARDER PTCOMA

<estructura_multidimensional> ::= CORIZQ <lista_estructuras> CORDER

<lista_estructuras> ::= <lista_estructuras> COMA <elemento_estructura>
                     | <elemento_estructura>

<elemento_estructura> ::= <estructura_multidimensional>
                       | CORIZQ <lista_elementos> CORDER

<lista_dimensiones> ::= <lista_dimensiones> COMA ENTERO
                     | ENTERO

<lista_valores> ::= <lista_valores> COMA <fila_vector>
                 | <lista_valores> COMA CORIZQ <lista_elementos> CORDER
                 | <fila_vector>
                 | CORIZQ <lista_elementos> CORDER

<fila_vector> ::= CORIZQ <lista_elementos> CORDER

<lista_elementos> ::= <lista_elementos> COMA <expresion>
                   | <expresion>

<vector_acceso> ::= ID <lista_indices>

<vector_asignacion> ::= ID <lista_indices> ASIGNACION <expresion> PTCOMA

<lista_indices> ::= <lista_indices> CORIZQ <expresion> CORDER
                 | CORIZQ <expresion> CORDER
                 | ε
```

### Procedimientos

```bnf
<expresion_procedimiento> ::= <proc_declaracion>
                           | <proc_llamada>

<proc_declaracion> ::= PROC ID PARIZQ <lista_parametros_opt> PARDER LLAVE_IZQ <lista_expresiones> LLAVE_DER

<proc_llamada> ::= EXEC ID PARIZQ <lista_argumentos_exec_opt> PARDER PTCOMA

<lista_parametros_opt> ::= <lista_parametros>
                        | ε

<lista_parametros> ::= <lista_parametros> COMA <tipo> DOSPUNTOS ID
                    | <tipo> DOSPUNTOS ID

<lista_argumentos_exec_opt> ::= <lista_argumentos_exec>
                             | ε

<lista_argumentos_exec> ::= <lista_argumentos_exec> COMA <argumento_exec>
                         | <argumento_exec>

<argumento_exec> ::= ID
                  | ENTERO
                  | DECIMAL
                  | CARACTER
                  | CADENA
                  | TRUE
                  | FALSE
```

### Declaraciones y Asignaciones

```bnf
<declaracion> ::= <tipo> ID PTCOMA

<asignacion> ::= ID ASIGNACION <expresion> PTCOMA
              | <tipo> ID ASIGNACION <expresion> PTCOMA

<println> ::= PRINTLN PARIZQ <expresion> PARDER PTCOMA
           | PRINTLN PARIZQ <expresion> PARDER
           | PRINTLN PARIZQ <oraciones> PARDER PTCOMA
           | PRINTLN PARIZQ <oraciones> PARDER

<oraciones> ::= <oraciones> ID
             | ID

<incremento_decremento> ::= ID INCREMENTO
                         | ID DECREMENTO

<tipo> ::= INT
        | FLOAT
        | CHAR
        | STRING
        | BOOL

<literal> ::= ENTERO
           | DECIMAL
           | CARACTER
           | CADENA
           | TRUE
           | FALSE

<comentario_multi_linea> ::= COMENTARIO_MULTILINEA

<comentario_una_linea> ::= COMENTARIO_UNA_LINEA
```

### Precedencia de Operadores

```bnf
<precedencia> ::= 
    1. NOT_LOGICO (asociatividad: derecha)
    2. OR_LOGICO (asociatividad: izquierda)
    3. AND_LOGICO (asociatividad: izquierda)
    4. XOR_LOGICO (asociatividad: izquierda)
    5. GE, LE, LT, GT, EQ, NE (asociatividad: izquierda)
    6. MAS, MENOS (asociatividad: izquierda)
    7. POR, DIVIDIDO, MODULO (asociatividad: izquierda)
    8. POTENCIA (asociatividad: derecha)
    9. UMINUS (asociatividad: derecha)
    10. CORIZQ, CORDER (asociatividad: izquierda)
```

## Análisis Léxico

### Tokens Soportados

- **Palabras Reservadas**: `int`, `float`, `char`, `string`, `bool`, `true`, `false`, `println`, `while`, `if`, `else`, `for`, `do`, `break`, `continue`, `switch`, `case`, `default`, `vector`, `seno`, `coseno`, `inv`, `proc`, `exec`, `shuffle`, `sort`
- **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `**`, `%`
- **Operadores Relacionales**: `>=`, `<=`, `<`, `>`, `==`, `!=`
- **Operadores Lógicos**: `||`, `&&`, `!`, `^`
- **Operadores de Incremento/Decremento**: `++`, `--`
- **Delimitadores**: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `:`
- **Literales**: enteros, decimales, caracteres, cadenas
- **Identificadores**: nombres de variables y funciones
- **Comentarios**: de una línea (`//`) y multilínea (`/* */`)

### Estados del Lexer

- **INITIAL**: Estado principal
- **comentario**: Estado para comentarios multilínea

## Análisis Sintáctico

### Características

- **Parser LR(1)** generado por PLY
- **Recuperación de errores** en modo pánico
- **Construcción automática del AST**
- **Manejo de precedencia** de operadores

### Reglas de Precedencia

```python
precedence = (
    ('right', 'NOT_LOGICO'),  
    ('left', 'OR_LOGICO'),  
    ('left', 'AND_LOGICO'),  
    ('left', 'XOR_LOGICO'),  
    ('left', 'GE', 'LE', 'LT', 'GT', 'EQ', 'NE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right', 'UMINUS'),
    ('left', 'CORIZQ', 'CORDER'),
)
```

## Análisis Semántico

### Verificaciones Realizadas

1. **Declaración de variables**: Verificar que las variables estén declaradas antes de su uso
2. **Compatibilidad de tipos**: Validar operaciones entre tipos compatibles
3. **Ámbito de variables**: Manejo de scopes en estructuras de control
4. **Vectores**: Validar dimensiones y accesos válidos
5. **Procedimientos**: Verificar parámetros y tipos de argumentos

### Tabla de Compatibilidad de Tipos

| Operación | int | float | char | string | bool |
|-----------|-----|-------|------|--------|------|
| **Suma** | ✓ | ✓ | ✓ | ✓ | ✗ |
| **Resta** | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Multiplicación** | ✓ | ✓ | ✓ | ✗ | ✗ |
| **División** | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Potencia** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Módulo** | ✓ | ✓ | ✗ | ✗ | ✗ |

## Estructuras de Datos

### Nodos del AST

```python
class Expresion:
    """Clase base para todos los nodos del AST"""
    def interpret(self):
        pass

class Numero(Expresion):
    def __init__(self, valor):
        self.valor = valor

class Suma(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
```

### Tabla de Símbolos

```python
class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.current_scope = 'global'
        self.scope_stack = ['global']
    
    def add_variable(self, name, data_type, value):
        # Implementación
        pass
    
    def get_variable(self, name):
        # Implementación
        pass
```

### Vectores Multidimensionales

Los vectores se almacenan como estructuras anidadas:

```python
# Vector 2D: Vector[int] matriz(2,2) = [[1,2],[3,4]]
{
    'tipo': 'vector',
    'subtipo': 'int',
    'dimensiones': [2, 2],
    'data': [[1, 2], [3, 4]]
}
```

## Manejo de Errores

### Tipos de Errores

1. **Errores Léxicos**: Caracteres no reconocidos
2. **Errores Sintácticos**: Violaciones de la gramática
3. **Errores Semánticos**: Violaciones de reglas semánticas

### Estrategias de Recuperación

- **Modo Pánico**: Descartar tokens hasta encontrar un símbolo de sincronización
- **Puntos de Sincronización**: `;`, `}`, palabras clave principales

### Ejemplo de Manejo de Errores

```python
def p_error(p):
    if p:
        errores_sintacticos.append({
            'tipo': 'Sintáctico',
            'descripcion': f"Token inesperado '{p.value}'",
            'linea': p.lineno,
            'columna': p.lexpos
        })
        # Modo pánico
        while True:
            tok = parser.token()
            if not tok or tok.type in ('PTCOMA', 'LLAVE_DER'):
                break
        parser.errok()
```

## Generación de Reportes

### Reportes Disponibles

1. **Tabla de Tokens**: Lista todos los tokens reconocidos
2. **Tabla de Variables**: Estado de todas las variables
3. **Tabla de Errores**: Errores léxicos, sintácticos y semánticos
4. **AST**: Representación gráfica del árbol de sintaxis abstracta

### Formato de Salida

Los reportes se generan en formato HTML con estilos CSS para mejor presentación:

```python
def graficar_tabla_tokens(codigo_fuente):
    # Genera reporte HTML de tokens
    pass

def graficar_ast(arboles, output_path='Reportes/AST'):
    # Genera diagrama del AST usando Graphviz
    pass
```

## Ejemplos de Uso

### Declaraciones de Variables

```c
int x = 5;
float y = 3.14;
char c = 'A';
string s = "Hola mundo";
bool b = true;
```

### Estructuras de Control

```c
// Condicional
if (x > 0) {
    println("Positivo");
} else {
    println("No positivo");
}

// Ciclo while
while (x > 0) {
    println(x);
    x--;
}

// Ciclo for
for (int i = 0; i < 10; i++) {
    println(i);
}
```

### Vectores

```c
// Vector unidimensional
Vector[int] v1(5) = [1, 2, 3, 4, 5];

// Vector bidimensional
Vector[int] matriz(2, 2) = [
    [1, 2],
    [3, 4]
];

// Acceso a elementos
println(matriz[0][1]); // Imprime 2

// Vector de 4 dimensiones
Vector[int] t4(2,2,2,2) = [
    [
        [ [1,2], [3,4] ],
        [ [5,6], [7,8] ]
    ],
    [
        [ [9,10], [11,12] ],
        [ [13,14], [15,16] ]
    ]
];

println(t4[0][0][0][0]); // Imprime 1
```

### Procedimientos

```c
proc sumar(int: a, int: b) {
    int resultado = a + b;
    println(resultado);
}

exec sumar(5, 3);
```

## Conclusiones

Este intérprete implementa un lenguaje de programación completo con:

- Soporte para múltiples tipos de datos
- Estructuras de control avanzadas
- Vectores multidimensionales (hasta 4 dimensiones)
- Procedimientos con parámetros
- Sistema robusto de manejo de errores
- Generación automática de reportes
- Interfaz web amigable

La arquitectura modular permite fácil extensión y mantenimiento del código.