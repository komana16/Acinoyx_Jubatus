import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Flask
from flask_login import LoginManager, login_manager

db = SQLAlchemy()   # Inicializando SALAlchemy 
DB_NAME = 'database.db' # Asignando el nombre de la base de daots

def crear_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1ab2c3d4e5f6g7'
    app.config['UPLOAD_FOLDER']="static/images"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, ur_lprefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .modelos import users, roles, posts, comments

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id))

    conn = sql.connect(DB_NAME)
    conn.close()
    return app

def create_database(app):
    if not path.exists('acinoyx_jubatus' + DB_NAME):
        db.create_all(app=app)
        print('Base de datos creada!')

"""     conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_photo TEXT, email TEXT, user_name TEXT, password TEXT, age INT, rol INT)')
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, photo TEXT, foot_note TEXT, post_date TEXT, user_id INT, FOREIGN KEY(user_id) REFERENCES users(id))')
    conn.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INT, comment TEXT, user_id INT, date TEXT, like INT, FOREIGN KEY(user_id) REFERENCES users(id) , FOREIGN KEY(post_id) REFERENCES posts(id))')
    conn.execute('CREATE TABLE IF NOT EXISTS roles (id INTEGER, rol TEXT)')
    
    conn.close()


    return app """