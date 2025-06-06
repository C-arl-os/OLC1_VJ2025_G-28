from parser import parser
from lexer import lexer

# Leer archivo de entrada
with open("entrada.txt", "r", encoding="utf-8") as f:
    entrada = f.read()

print("----- ENTRADA -----")
print(entrada)

print("\n----- SALIDA DEL PARSER -----")
parser.parse(entrada, lexer=lexer)
