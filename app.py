from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Lista para almacenar mensajes de contacto
contact_messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Guardar el mensaje en la lista
        contact_messages.append({'name': name, 'email': email, 'message': message})
        flash('Mensaje enviado con éxito!', 'success')
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html', messages=contact_messages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
