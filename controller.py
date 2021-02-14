from flask import request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import safe_str_cmp
from flask import jsonify

# local imports
from init import app
from model import db, Usuario, Usuario_Schema, Restaurante, Restaurante_Schema

# Security
def authenticate(email, password):
    user = Usuario.query.filter_by(email=email).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return True
    else:
        return False


# App instances
api = Api(app)
jwt = JWTManager(app)

# Model instancies
usuario_schema = Usuario_Schema()
restaurante_schema = Restaurante_Schema()


class RecursosRestaurante(Resource):
    
    @jwt_required()
    def post(self):
        nuevo_restaurante = Restaurante(
            name = request.json['name'],
            category = request.json['category'],
            city = request.json['city'],
            location = request.json['location'],
            tel = request.json['tel'],
            delivery = request.json['delivery'],
            owner = get_jwt_identity() 
        )
        db.session.add(nuevo_restaurante)
        db.session.commit()
        return restaurante_schema.dump(nuevo_restaurante)

class RecursosUsuario(Resource):

    def post(self):
        nuevo_usuario = Usuario(
            email = request.json['email'],
            password = request.json['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return restaurante_schema.dump(nuevo_usuario)

class Login(Resource):

    def get(self):
        email = request.json['email'],
        password = request.json['password']
        value = authenticate(email, password)
        if value:
            return jsonify(access_token=create_access_token(identity=email))
        else:
            return "Correo electrónico o contraseña incorrectos"


api.add_resource(RecursosRestaurante, '/restaurante')
api.add_resource(RecursosUsuario, '/registrar')
api.add_resource(Login, '/login')

# Execution
if __name__ == '__main__':
    app.run(debug=True)