#Aqui se definen y se guardan las rutas estandar de la pagina (a donde los usuarios pueden ir)
import os
import sqlite3 as sql
import datetime
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask.helpers import url_for  #Estos importes permiten tener este archivo como un plano para la pagina (Blueprint), a renderizar las vistas html
                                                              #A pedir informacion (request) y mostrar mensajes en la pantalla (flash)

views = Blueprint('views', __name__)    #Asi es como se definira el "plano" (Blueprint)
basedir = os.path.abspath(os.path.dirname(__file__))

@views.route('/', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@views.route('/feed', methods=['GET', 'POST'])
def feed():

    # Data for tests
    #posts = []
    #post1 = {
    #    'user_id': 'Karina Omana',
    #    'foot_note': 'Mi primer post',
    #    'photo': "La foto"
    #}
    #post2 = {
    #    'user_id': 'Mariale',
    #    'foot_note': 'Mi segundo post',
    #    'photo': "La foto"
    #}
    #post3 = {
    #    'user_id': 'Eduardo',
    #    'foot_note': 'Mi tercer post',
    #}
    #posts.append(post1)
    #posts.append(post2)
    #posts.append(post3)
    #data = posts

    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(
        """
        SELECT t1.photo, t1.foot_note, t1.post_date, t2.user_name
        FROM posts t1
        LEFT JOIN users t2 on t1.user_id = t2.id 
        """
    )
    data = cur.fetchall()
    con.close()

    return render_template("feed.html", posts=data)

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
                return redirect(url_for("views.feed"))

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

@views.route('/post', methods=['GET', 'POST'])
def post():

    if request.method == 'POST':
        post_title = request.form['title']
        post_user = 1
        post_date = datetime.datetime.now()
        upload_image = request.files['upload_image']
        if upload_image.filename != '':
            filepath = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
        
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("INSERT INTO posts(photo, foot_note, post_date, user_id) VALUES(?,?,?,?)",
            (upload_image.filename, post_title, post_date, post_user)
        )
        con.commit()
        flash("Publicacion creada!")

        return redirect(url_for("views.feed"))


    return render_template("crear_post.html")

