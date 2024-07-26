from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from db import db

class Usuarios(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True, nullable=False)
    nombre_usuario=db.Column(db.String(45), nullable=False)
    contrasenia=db.Column(db.String(45), nullable=False)
    es_admin=db.Column(db.Boolean, nullable=False)
    es_empleado=db.Column(db.Boolean, nullable=False)