from parser import parser, comentarios  # importa la lista también

def analizar_texto(texto):
    resultado = []
    comentarios.clear()  # Limpiar comentarios anteriores

    for linea in texto.splitlines():
        if not linea.strip():
            continue
        raiz = parser.parse(linea)
        if raiz is None:
            #por alguna razón da error, lo comentaré mientras aprendemos el porque
            #resultado.append("Hubo un error al parsear la expresión.")
            continue
        if hasattr(raiz, 'interpret'):
            resultado.append(f"Expresión: {raiz}")
            resultado.append(f"Resultado: {raiz.interpret()}")

    resultado.extend(comentarios)  # Añadir los comentarios al final
    return '\n'.join(resultado)

#LEER POR FAVOR
# PARA HACERLO FUNCIONAR
# ESCRIBIR PYTHON APP.PY HUBICADOS EN LA CARPETA "INTERPRETER"