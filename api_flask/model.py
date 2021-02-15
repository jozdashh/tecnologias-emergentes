from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy

# local imports
from init import app

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))

class Usuario_Schema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str()


class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(20))
    city = db.Column(db.String(50))
    location = db.Column(db.String(100))
    tel = db.Column(db.String(10))
    delivery = db.Column(db.Boolean)
    owner = db.Column(db.String(50))

class Restaurante_Schema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()
    category = fields.Str()
    city = fields.Str()
    location = fields.Str()
    tel = fields.Str()
    delivery = fields.Bool()
    owner = fields.Str()

class Imagen(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(50))
	restaurant = db.Column(db.String(50))
	owner = db.Column(db.String(50))

class Imagen_Schema(Schema):
	id = fields.Int(dump_only = True)
	filename = fields.Str()
	restaurant = fields.Str()
	owner = fields.Str()
	
