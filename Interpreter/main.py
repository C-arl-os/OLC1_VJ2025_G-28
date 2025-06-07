from parser import parser
from lexer import lexer


def imprimir_tokens(codigo):
    lexer.input(codigo)
    print("Tokens:\n")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type:<12} → {tok.value}")

def main():
    codigo = '''
        int a = 5;
        float pi = 3.14;
        char letra = 'x';
        string saludo = "hola mundo";
        bool activo = true;
    '''

    print("prueba:\n\t", codigo.strip(), "\n")
    
    imprimir_tokens(codigo)

if __name__ == "__main__":
    main()