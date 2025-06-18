from flask import Flask, render_template, request, send_from_directory
from main import analizar_texto  # Aquí importas la función
from parser import parser, comentarios, errores_sintacticos
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado = ''
    if request.method == 'POST':
        texto = request.form['codigo'].lower()
        resultado = analizar_texto(texto)
    return render_template('index.html', resultado=resultado)

@app.route('/reportes/<path:filename>')
def reportes_static(filename):
    # Obtiene la ruta absoluta de la carpeta Reportes
    reportes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Reportes')
    return send_from_directory(reportes_dir, filename)

if __name__ == '__main__':
    print("Servidor Flask iniciado en http://127.0.0.1:5000")
    app.run(debug=True)
