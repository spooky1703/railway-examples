import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

contact_messages = []

API_KEY = 'c5065d56d8b04794c2ea510d959b0d3e'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Por favor completa todos los campos', 'danger')
        else:
            contact_messages.append({'name': name, 'email': email, 'message': message})
            flash('Mensaje enviado con éxito!', 'success')
            return redirect(url_for('contacto'))
    
    return render_template('contacto.html', messages=contact_messages)

@app.route('/clima', methods=['GET', 'POST'])
def clima():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash('Por favor ingresa una ciudad', 'danger')
        else:
            try:
                params = {
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric',
                    'lang': 'es'  # Para obtener descripciones en español
                }
                response = requests.get(BASE_URL, params=params)
                
                if response.status_code == 200:
                    weather_data = response.json()
                elif response.status_code == 404:
                    flash('Ciudad no encontrada. Intenta con otro nombre.', 'danger')
                else:
                    flash(f'Error al consultar el clima: {response.status_code}', 'danger')
                    
            except requests.exceptions.RequestException as e:
                flash(f'Error de conexión: {str(e)}', 'danger')
    
    return render_template('clima.html', weather_data=weather_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
