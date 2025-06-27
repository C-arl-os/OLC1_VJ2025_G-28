# Lista global para advertencias del analizador
advertencias = []

def agregar_advertencia(tipo, descripcion, linea=-1, columna=-1):
    """Agrega una advertencia a la lista global"""
    advertencias.append({
        'tipo': tipo,
        'descripcion': descripcion,
        'linea': linea,
        'columna': columna
    })

def limpiar_advertencias():
    """Limpia la lista de advertencias"""
    advertencias.clear()

def obtener_advertencias():
    """Obtiene la lista actual de advertencias"""
    return advertencias.copy()
