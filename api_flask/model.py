from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# local imports
from init import app

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))

class Usuario_Schema(ma.Schema):
    class Meta:
        field = ('email', 'password')


class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(20))
    city = db.Column(db.String(50))
    location = db.Column(db.String(100))
    tel = db.Column(db.String(10))
    delivery = db.Column(db.Boolean)
    owner = db.Column(db.String(50))

class Restaurante_Schema(ma.Schema):
    
    class Meta:
        field = ('id', 'name', 'category', 'city', 'location', 'tel', 'delivery')