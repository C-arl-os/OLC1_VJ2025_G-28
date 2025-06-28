# Manual de Usuario - Intérprete OLC1_VJ2025_G-28

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Interfaz de Usuario](#interfaz-de-usuario)
4. [Sintaxis del Lenguaje](#sintaxis-del-lenguaje)
5. [Tipos de Datos](#tipos-de-datos)
6. [Variables y Declaraciones](#variables-y-declaraciones)
7. [Operadores](#operadores)
8. [Estructuras de Control](#estructuras-de-control)
9. [Vectores](#vectores)
10. [Procedimientos](#procedimientos)
11. [Funciones Especiales](#funciones-especiales)
12. [Comentarios](#comentarios)
13. [Ejemplos Completos](#ejemplos-completos)
14. [Reportes](#reportes)
15. [Manejo de Errores](#manejo-de-errores)
16. [Preguntas Frecuentes](#preguntas-frecuentes)

## Introducción

Este manual describe el uso del intérprete desarrollado para el curso de Organización de Lenguajes y Compiladores 1. El intérprete permite ejecutar código en un lenguaje similar a C con características adicionales como vectores multidimensionales y procedimientos.

### Características Principales

- **Tipos de datos primitivos**: enteros, decimales, caracteres, cadenas y booleanos
- **Estructuras de control**: if-else, while, do-while, for, switch-case
- **Vectores multidimensionales**: soporte hasta 4 dimensiones
- **Procedimientos**: funciones definidas por el usuario
- **Operadores**: aritméticos, relacionales y lógicos
- **Funciones matemáticas**: seno, coseno, inversa
- **Interfaz web**: editor de código integrado con reportes

## Instalación y Configuración

### Requisitos del Sistema

- **Python 3.8 o superior**
- **PLY (Python Lex-Yacc)**
- **Flask**
- **Graphviz**

### Instalación

1. **Instalar Python** (si no está instalado):
   ```bash
   # Windows: Descargar desde https://python.org
   # Linux/Mac: usar el gestor de paquetes del sistema
   ```

2. **Instalar dependencias**:
   ```bash
   pip install ply flask graphviz
   ```

3. **Ejecutar el intérprete**:
   ```bash
   cd OLC1_VJ2025_G-28/Interpreter
   python app.py
   ```

4. **Abrir navegador**:
   ```
   http://127.0.0.1:5000
   ```

## Interfaz de Usuario

La interfaz web consta de los siguientes elementos:

### Editor de Código
- **Área de texto grande** para escribir el código fuente
- **Botón "Analizar"** para procesar el código
- **Área de resultados** que muestra la salida del programa

### Botones de Reportes
- **Ver Tokens**: Muestra todos los tokens reconocidos
- **Ver Variables**: Estado actual de todas las variables
- **Ver Errores**: Lista de errores encontrados
- **Ver Advertencias**: Advertencias del compilador
- **Ver AST**: Árbol de sintaxis abstracta en formato PDF

### Área de Resultados
Muestra la salida del programa, incluyendo:
- Valores impresos con `println`
- Mensajes de error
- Estado de variables

## Sintaxis del Lenguaje

### Estructura General

```c
// Comentarios de una línea
/* Comentarios
   de múltiples líneas */

// Declaraciones de variables
int x;
float y = 3.14;

// Estructuras de control
if (condicion) {
    // código
}

// Función principal implícita
println("Hola mundo");
```

### Reglas Sintácticas

- **Punto y coma obligatorio** al final de cada instrucción
- **Llaves `{}` obligatorias** para bloques de código
- **Paréntesis `()` obligatorios** en condiciones
- **Sensible a mayúsculas y minúsculas**

## Tipos de Datos

### Tipos Primitivos

| Tipo | Descripción | Ejemplo | Valor por Defecto |
|------|-------------|---------|-------------------|
| `int` | Números enteros | `42`, `-15` | `0` |
| `float` | Números decimales | `3.14`, `-2.5` | `0.0` |
| `char` | Caracteres individuales | `'A'`, `'z'` | `'\0'` |
| `string` | Cadenas de texto | `"Hola"`, `"mundo"` | `""` |
| `bool` | Valores lógicos | `true`, `false` | `false` |

### Ejemplos de Declaración

```c
// Declaraciones simples
int edad;
float peso;
char inicial;
string nombre;
bool activo;

// Declaraciones con inicialización
int x = 10;
float pi = 3.14159;
char letra = 'A';
string saludo = "Hola mundo";
bool verdadero = true;
```

## Variables y Declaraciones

### Declaración de Variables

```c
// Sintaxis: tipo nombre;
int numero;
float decimal;
char caracter;
string texto;
bool booleano;
```

### Asignación de Variables

```c
// Declaración con asignación
int x = 5;

// Asignación posterior
int y;
y = 10;

// Reasignación
x = 20;
```

### Reglas de Nombres

- Deben comenzar con una **letra** (a-z, A-Z)
- Pueden contener **letras**, **números** y **guiones bajos** (_)
- **No pueden** ser palabras reservadas
- Son **sensibles a mayúsculas y minúsculas**

**Válidos**: `miVariable`, `contador1`, `nombre_completo`
**Inválidos**: `1numero`, `if`, `mi-variable`

## Operadores

### Operadores Aritméticos

| Operador | Descripción | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `+` | Suma | `5 + 3` | `8` |
| `-` | Resta | `5 - 3` | `2` |
| `*` | Multiplicación | `5 * 3` | `15` |
| `/` | División | `5 / 2` | `2.5` |
| `**` | Potencia | `2 ** 3` | `8` |
| `%` | Módulo | `5 % 3` | `2` |
| `-` | Negación unaria | `-5` | `-5` |

### Operadores Relacionales

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `==` | Igual a | `x == 5` |
| `!=` | Diferente de | `x != 5` |
| `>` | Mayor que | `x > 5` |
| `<` | Menor que | `x < 5` |
| `>=` | Mayor o igual | `x >= 5` |
| `<=` | Menor o igual | `x <= 5` |

### Operadores Lógicos

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `&&` | AND lógico | `(x > 0) && (y < 10)` |
| `\|\|` | OR lógico | `(x == 0) \|\| (y == 0)` |
| `!` | NOT lógico | `!(x == 0)` |
| `^` | XOR lógico | `true ^ false` |

### Operadores de Incremento/Decremento

```c
int x = 5;
x++;  // x = 6 (post-incremento)
x--;  // x = 5 (post-decremento)
```

### Precedencia de Operadores

1. `()` (paréntesis)
2. `!` (negación lógica)
3. `**` (potencia)
4. `*`, `/`, `%` (multiplicación, división, módulo)
5. `+`, `-` (suma, resta)
6. `<`, `<=`, `>`, `>=` (relacionales)
7. `==`, `!=` (igualdad)
8. `&&` (AND lógico)
9. `^` (XOR lógico)
10. `||` (OR lógico)

## Estructuras de Control

### Condicional IF

```c
// IF simple
if (condicion) {
    // código
}

// IF-ELSE
if (condicion) {
    // código si verdadero
} else {
    // código si falso
}

// IF-ELSE IF
if (condicion1) {
    // código 1
} else if (condicion2) {
    // código 2
} else {
    // código por defecto
}
```

**Ejemplo:**
```c
int edad = 18;

if (edad >= 18) {
    println("Es mayor de edad");
} else {
    println("Es menor de edad");
}
```

### Ciclo WHILE

```c
while (condicion) {
    // código que se repite
}
```

**Ejemplo:**
```c
int contador = 1;
while (contador <= 5) {
    println(contador);
    contador++;
}
```

### Ciclo DO-WHILE

```c
do {
    // código que se ejecuta al menos una vez
} while (condicion);
```

**Ejemplo:**
```c
int numero;
do {
    println("Ingrese un número positivo");
    numero = 5; // simulación de entrada
} while (numero <= 0);
```

### Ciclo FOR

```c
// Con declaración de variable
for (tipo variable = inicial; condicion; actualizacion) {
    // código
}

// Con variable existente
for (variable = inicial; condicion; actualizacion) {
    // código
}
```

**Ejemplo:**
```c
// Imprimir números del 1 al 10
for (int i = 1; i <= 10; i++) {
    println(i);
}
```

### Estructura SWITCH

```c
switch (expresion) {
    case valor1:
        // código para valor1
        break;
    case valor2:
        // código para valor2
        break;
    default:
        // código por defecto
        break;
}
```

**Ejemplo:**
```c
int dia = 3;
switch (dia) {
    case 1:
        println("Lunes");
        break;
    case 2:
        println("Martes");
        break;
    case 3:
        println("Miércoles");
        break;
    default:
        println("Otro día");
        break;
}
```

### Control de Flujo

```c
// BREAK: sale del ciclo
for (int i = 1; i <= 10; i++) {
    if (i == 5) {
        break; // Sale cuando i = 5
    }
    println(i);
}

// CONTINUE: salta a la siguiente iteración
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue; // Salta cuando i = 3
    }
    println(i);
}
```

## Vectores

### Declaración de Vectores

```c
// Vector unidimensional
Vector[tipo] nombre(tamaño);

// Vector multidimensional
Vector[tipo] nombre(dim1, dim2, ...);
```

### Ejemplos de Declaración

```c
// Vector de enteros de tamaño 5
Vector[int] numeros(5);

// Matriz 3x3 de decimales
Vector[float] matriz(3, 3);

// Vector tridimensional
Vector[int] cubo(2, 2, 2);

// Vector de 4 dimensiones
Vector[int] hipercubo(2, 2, 2, 2);
```

### Inicialización de Vectores

```c
// Vector unidimensional con valores
Vector[int] numeros(5) = [1, 2, 3, 4, 5];

// Matriz bidimensional
Vector[int] matriz(2, 2) = [
    [1, 2],
    [3, 4]
];

// Vector tridimensional
Vector[int] cubo(2, 2, 2) = [
    [
        [1, 2],
        [3, 4]
    ],
    [
        [5, 6],
        [7, 8]
    ]
];

// Vector de 4 dimensiones
Vector[int] t4(2, 2, 2, 2) = [
    [
        [ [1,2], [3,4] ],
        [ [5,6], [7,8] ]
    ],
    [
        [ [9,10], [11,12] ],
        [ [13,14], [15,16] ]
    ]
];
```

### Acceso a Elementos

```c
// Leer elemento
int valor = matriz[0][1];

// Asignar elemento
matriz[1][0] = 10;

// Vectores multidimensionales
int elemento = t4[0][1][0][1];
```

### Operaciones Especiales

```c
// Vector ordenado (SORT)
Vector[int] original(4) = [3, 1, 4, 2];
Vector[int] ordenado(4) = sort(original);
// ordenado contiene: [1, 2, 3, 4]

// Vector transpuesto (SHUFFLE)
Vector[int] matriz(2, 3) = [
    [1, 2, 3],
    [4, 5, 6]
];
Vector[int] transpuesta(3, 2) = shuffle(matriz);
// transpuesta contiene: [[1,4], [2,5], [3,6]]
```

## Procedimientos

### Declaración de Procedimientos

```c
proc nombre(tipo1: parametro1, tipo2: parametro2, ...) {
    // código del procedimiento
}
```

### Llamada a Procedimientos

```c
exec nombre(argumento1, argumento2, ...);
```

### Ejemplos

```c
// Procedimiento sin parámetros
proc saludar() {
    println("¡Hola mundo!");
}

// Procedimiento con parámetros
proc sumar(int: a, int: b) {
    int resultado = a + b;
    println("La suma es: ");
    println(resultado);
}

// Procedimiento con múltiples tipos
proc mostrarInfo(string: nombre, int: edad, bool: activo) {
    println("Nombre: ");
    println(nombre);
    println("Edad: ");
    println(edad);
    println("Activo: ");
    println(activo);
}

// Llamadas a procedimientos
exec saludar();
exec sumar(5, 3);
exec mostrarInfo("Juan", 25, true);
```

## Funciones Especiales

### Función println

```c
// Imprimir diferentes tipos de datos
println("Texto");
println(42);
println(3.14);
println('A');
println(true);

// Imprimir variables
int x = 10;
println(x);
```

### Funciones Matemáticas

```c
// Seno (en radianes)
float resultado1 = seno(1.57); // ≈ 1.0

// Coseno (en radianes)
float resultado2 = coseno(0); // = 1.0

// Inversa (invierte dígitos)
int numero = 123;
int invertido = inv(numero); // = 321
```

### Ejemplos de Uso

```c
// Calcular seno y coseno
float angulo = 1.57; // π/2 radianes
float sen = seno(angulo);
float cos = coseno(angulo);

println("Seno: ");
println(sen);
println("Coseno: ");
println(cos);

// Invertir un número
int original = 12345;
int invertido = inv(original);
println("Original: ");
println(original);
println("Invertido: ");
println(invertido);
```

## Comentarios

### Comentarios de Una Línea

```c
// Este es un comentario de una línea
int x = 5; // Comentario al final de la línea
```

### Comentarios de Múltiples Líneas

```c
/*
Este es un comentario
de múltiples líneas
que puede abarcar
varias líneas
*/

int y = 10;

/*
Los comentarios pueden estar
en cualquier parte del código
*/
```

## Ejemplos Completos

### Ejemplo 1: Calculadora Básica

```c
// Calculadora básica
int a = 10;
int b = 5;

println("Números: ");
println(a);
println(b);

int suma = a + b;
int resta = a - b;
int mult = a * b;
float div = a / b;

println("Suma: ");
println(suma);
println("Resta: ");
println(resta);
println("Multiplicación: ");
println(mult);
println("División: ");
println(div);
```

### Ejemplo 2: Tabla de Multiplicar

```c
// Tabla de multiplicar del 5
int numero = 5;
println("Tabla del 5:");

for (int i = 1; i <= 10; i++) {
    int resultado = numero * i;
    println(numero);
    println(" x ");
    println(i);
    println(" = ");
    println(resultado);
}
```

### Ejemplo 3: Manejo de Vectores

```c
// Trabajando con matrices
Vector[int] matriz(3, 3) = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

println("Matriz original:");
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        println(matriz[i][j]);
    }
}

// Modificar un elemento
matriz[1][1] = 99;
println("Elemento central modificado: ");
println(matriz[1][1]);
```

### Ejemplo 4: Procedimientos

```c
// Definir procedimientos
proc calcularArea(int: base, int: altura) {
    int area = base * altura;
    println("El área es: ");
    println(area);
}

proc mostrarMenu() {
    println("=== MENÚ ===");
    println("1. Calcular área");
    println("2. Salir");
}

// Usar procedimientos
exec mostrarMenu();
exec calcularArea(10, 5);
```

## Reportes

La interfaz web genera automáticamente varios reportes:

### Tabla de Tokens
Muestra todos los tokens reconocidos con:
- **Lexema**: El texto original
- **Token**: Tipo de token reconocido
- **Línea**: Número de línea
- **Columna**: Posición en la línea

### Tabla de Variables
Muestra el estado actual de todas las variables:
- **Variable**: Nombre de la variable
- **Valor**: Valor actual almacenado

### Tabla de Errores
Lista todos los errores encontrados:
- **Tipo**: Léxico, Sintáctico o Semántico
- **Descripción**: Explicación del error
- **Línea**: Ubicación del error
- **Columna**: Posición específica

### Árbol de Sintaxis Abstracta (AST)
Representación gráfica en PDF del árbol de análisis sintáctico.

### Tabla de Advertencias
Muestra advertencias no críticas del compilador.

## Manejo de Errores

### Tipos de Errores

#### Errores Léxicos
- **Caracteres no reconocidos**
- **Comentarios malformados**
- **Cadenas sin cerrar**

```c
// Error: carácter no válido
int x = 5@; // Error léxico: '@' no reconocido
```

#### Errores Sintácticos
- **Falta de punto y coma**
- **Paréntesis no balanceados**
- **Palabras clave mal usadas**

```c
// Error: falta punto y coma
int x = 5  // Error sintáctico

// Error: paréntesis no balanceados
if (x > 0 {  // Error sintáctico
    println(x);
}
```

#### Errores Semánticos
- **Variables no declaradas**
- **Tipos incompatibles**
- **Índices fuera de rango**

```c
// Error: variable no declarada
println(y); // Error semántico: 'y' no declarada

// Error: tipos incompatibles
bool resultado = 5 + "texto"; // Error semántico
```

### Estrategias de Corrección

1. **Revisar la sintaxis** básica (punto y coma, llaves, paréntesis)
2. **Verificar declaraciones** de variables antes de su uso
3. **Validar tipos** en operaciones y asignaciones
4. **Comprobar límites** de vectores y matrices
5. **Revisar parámetros** en llamadas a procedimientos

## Preguntas Frecuentes

### ¿Cómo ejecuto el intérprete?

```bash
cd OLC1_VJ2025_G-28/Interpreter
python app.py
```
Luego abre http://127.0.0.1:5000 en tu navegador.

### ¿Por qué mi código no compila?

Verifica:
- Punto y coma al final de cada instrucción
- Llaves balanceadas en bloques de código
- Variables declaradas antes de su uso
- Tipos de datos correctos

### ¿Cómo declaro un vector multidimensional?

```c
// Sintaxis general
Vector[tipo] nombre(dim1, dim2, dim3, ...);

// Ejemplo: matriz 4x4
Vector[int] matriz(4, 4);
```

### ¿Puedo usar vectores de más de 4 dimensiones?

No, el intérprete soporta hasta 4 dimensiones máximo.

### ¿Cómo accedo a los reportes?

Después de analizar el código, usa los botones en la interfaz:
- "Ver Tokens"
- "Ver Variables"
- "Ver Errores"
- "Ver AST"

### ¿El lenguaje es sensible a mayúsculas?

Sí, `Variable` y `variable` son identificadores diferentes.

### ¿Puedo definir funciones que retornen valores?

No, solo se soportan procedimientos (proc) que no retornan valores.

### ¿Cómo imprimo múltiples valores en una línea?

Actualmente, cada `println` imprime en una línea separada. Para imprimir en la misma línea, concatena los valores:

```c
string mensaje = "El resultado es: " + 42;
println(mensaje);
```

---

**Versión del Manual**: 1.0  
**Fecha**: Junio 2025  
**Proyecto**: OLC1_VJ2025_G-28