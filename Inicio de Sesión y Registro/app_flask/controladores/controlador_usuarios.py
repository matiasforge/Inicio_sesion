from flask import render_template, request, redirect, session, flash
from app_flask.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt
from app_flask import app

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def despliega_registro_login():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def despliega_home():
    if 'id_usuario' not in session:
        return redirect('/')
    return render_template('home.html')

@app.route('/procesa/registro', methods=['POST'])
def procesa_registro():
    if Usuario.valida_registro(request.form) == False:
        return redirect('/')
    password_encriptado = bcrypt.generate_password_hash(request.form['password'])
    nuevo_usuario = {
        **request.form,
        'password' : password_encriptado
    }
    id_usuario = Usuario.crear_uno(nuevo_usuario)
    session['nombre'] = request.form['nombre']
    session['apellido'] = request.form['apellido']
    session['id_usuario'] = id_usuario

    return redirect('/home')

@app.route('/procesa/login', methods=['POST'])
def procesa_login():
    usuario = Usuario.obtener_uno(request.form)
    if usuario == None:
        flash('Usuario no encontrado.', 'error_login')
        return redirect('/')
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash('Credenciales inválidas.', 'error_login')
        return redirect('/')
    session['nombre'] = usuario.nombre
    session['apellido'] = usuario.apellido
    session['id_usuario'] = usuario.id
    return redirect('/home')

@app.route('/procesa/logout', methods=['POST'])
def procesa_logout():
    session.clear()
    return redirect('/')
    



