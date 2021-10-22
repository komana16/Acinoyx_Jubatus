#Aqui se definen y se guardan las rutas estandar de la pagina (a donde los usuarios pueden ir)
import sqlite3 as sql
from flask import Blueprint, render_template, request, flash  #Estos importes permiten tener este archivo como un plano para la pagina (Blueprint), a renderizar las vistas html
                                                              #A pedir informacion (request) y mostrar mensajes en la pantalla (flash)

views = Blueprint('views', __name__)    #Asi es como se definira el "plano" (Blueprint)

@views.route('/', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@views.route('/feed', methods=['GET', 'POST'])
def feed():
    return render_template("feed.html")

@views.route('/resultados_busqueda', methods=['GET', 'POST'])
def resultados_busqueda():
    return render_template("resultados_busqueda.html")

@views.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':
        name = request.form['nombre']
        email = request.form['correo']
        age = request.form['edad']
        password = request.form['Contraseña']

        print(name,email,age,password)
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT email FROM users WHERE email = '{}'".format(email))

            data = cur.fetchone()
            if data :
                flash("este correo ya esta registrado")
            else:
                cur.execute('INSERT INTO users (user_name, email, age, password) VALUES (?,?,?,?)',(name,email,age, password))
                con.commit()
                flash("registro exitoso")
                return render_template("feed.html")



    return render_template("registro.html")


@views.route('/dashboard_administrativo', methods=['GET', 'POST'])
def dashboard_administrativo():
    return render_template("dashboard_administrativo.html")

@views.route('/detalle_post_general', methods=['GET', 'POST'])
def detalle_post_general():
    return render_template("detalle_post_general.html")

@views.route('/detalle_post_2', methods=['GET', 'POST'])
def detalle_post_2():
    return render_template("detalle_post_2.html")

