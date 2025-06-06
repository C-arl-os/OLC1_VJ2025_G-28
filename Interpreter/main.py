from parser import parser

def main():
    texto = """3 / 4 - 2 + 7 - 5
int x = 1.5 + 2.5 - 0.5 * 4.1 - 1.0;
"""

    for linea in texto.splitlines():
        if not linea.strip():
            continue
        raiz = parser.parse(linea)
        if raiz is None:
            print("Hubo un error al parsear la expresión.")
            continue
        print("Representación infija (con paréntesis):", raiz)
        valor = raiz.interpret()
        print("Resultado numérico:", valor)

if __name__ == "__main__":
    main()
