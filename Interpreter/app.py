from flask import Flask, render_template, request
from main import analizar_texto  # Aquí importas la función

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado = ''
    if request.method == 'POST':
        texto = request.form['codigo']
        resultado = analizar_texto(texto)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    print("Servidor Flask iniciado en http://127.0.0.1:5000")
    app.run(debug=True)
