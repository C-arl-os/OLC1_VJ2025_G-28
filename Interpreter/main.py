from parser import parser

def main():
<<<<<<< HEAD
    texto = """3 / 4 - 2 + 7 - 5
int x = 1.5 + 2.5 - 0.5 * 4.1 - 1.0;
"""
=======
    texto = "//comentario prueba\n//comentario prueba 2\n/*salto\nlinea*/"
>>>>>>> Operaciones

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
