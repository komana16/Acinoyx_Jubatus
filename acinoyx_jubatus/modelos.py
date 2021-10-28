from datetime import timezone
from acinoyx_jubatus import db  # La base de datos de __init__ es importada
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey, create_engine, engine
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

""" engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)()

Base = declarative_base() """

class users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_photo = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  # Unique = True hace que no sea posible que dos usuarios tengan el mismo correo
    user_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    age = db.Column(db.String(3))
    rol = db.Column(db.Integer)
    user_post = relationship("posts", backref="users")
    user_comment = relationship("comments", backref="users")
    
class roles(db.Model, UserMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(150))


class posts(db.Model, UserMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(150))
    foot_note = db.Column(db.String(150))
    post_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(Integer, ForeignKey('users.id'))
    post_comment = relationship("comments", backref="posts")

class comments(db.Model, UserMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(Integer, ForeignKey('posts.id'))
    comment = db.Column(db.String(10000)) 
    user_id = db.Column(Integer, ForeignKey('users.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    like = db.Column(db.Integer)