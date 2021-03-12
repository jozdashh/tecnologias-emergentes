from flask import request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import safe_str_cmp
from flask import jsonify
from google.cloud import storage
from urllib.parse import quote_plus
import os

# local imports
from init import app
from model import db, Usuario, Usuario_Schema, Restaurante, Restaurante_Schema, Imagen, Imagen_Schema

# Setting credentials using the downloaded JSON file
client = storage.Client.from_service_account_json(json_credentials_path='credentials-python-storage.json')
# Creating bucket object
bucket = client.get_bucket('flask-bucket-app')

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
restaurantes_schema = Restaurante_Schema(many=True)
imagen_schema = Imagen_Schema()

class RecursoNuevoRestaurante(Resource):
	# Crear un nuevo restaurante
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

class RecursoBorrarRestaurante(Resource):
	# Eliminar un restaurante existente
	@jwt_required()
	def delete(self, restaurante_id):
		# name = request.json['name']
		# restaurante = Restaurante.query.filter_by(name=name).first()
		restaurante = Restaurante.query.filter_by(id=restaurante_id).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
			db.session.delete(restaurante)
			db.session.commit()
			return jsonify(restaurante_schema.dump(restaurante))
		else:
			return "El restaurante a eliminar no existe o no es el dueño"

class RecursoRestaurante(Resource):
	# Retornar todos los restaurantes del usuario actual
	@jwt_required()
	def get(self):
		owner = get_jwt_identity()[0]
		restaurantes = Restaurante.query.filter_by(owner=owner)
		return restaurantes_schema.dump(restaurantes)
	
	# Buscar restaurantes creados por nombre
	@jwt_required()
	def post(self):
		name = request.json['name']
		restaurante = Restaurante.query.filter_by(name=name).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
		  return restaurante_schema.dump(restaurante)
		else:
		  return "El restaurante a detallar no existe o no es el dueño"

	# Modificar un restaurante existente
	@jwt_required()
	def put(self):
		name = request.json['name']
		restaurante = Restaurante.query.filter_by(name=name).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
			new_name = request.json['name']
			restaurante.name = new_name

			new_category = request.json['category']
			restaurante.category = new_category

			new_city = request.json['city']
			restaurante.category = new_city

			new_location = request.json['location']
			restaurante.location = new_location

			new_tel = request.json['tel']
			restaurante.tel = new_tel

			new_delivery = request.json['delivery']
			restaurante.tel = new_delivery

			db.session.commit()
			return restaurante_schema.dump(restaurante)

		else:
			return "El restaurante a editar no existe o no es el dueño"

class RecursoRegistro(Resource):
	# Registrar un nuevo usuario
	def post(self):
		nuevo_usuario = Usuario(
			email = request.json['email'],
			password = request.json['password']
		)
		db.session.add(nuevo_usuario)
		db.session.commit()
		return restaurante_schema.dump(nuevo_usuario)

class RecursoLogin(Resource):
	# Recibir token de autenticación para hacer login
	def post(self):
		email = request.json['email'],
		password = request.json['password']
		value = authenticate(email, password)
		if value:
		  return jsonify(access_token=create_access_token(identity=email))
		else:
		  return "Correo electrónico o contraseña incorrectos"

class RecursoNuevoArchivo(Resource):
	# Subir nueva imagen para restaurante
	@jwt_required()
	def post(self, restaurante_id):
		restaurante = Restaurante.query.filter_by(id=restaurante_id).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
			folder_path = restaurante.owner + '/' + restaurante.name + '/'
			file = request.files['file']
			if storage.Blob(bucket=bucket, name=folder_path+file.filename).exists(client):
				return "El archivo ya se encuentra almacenado"
			elif file.filename == None or len(file.filename) == 0:
				return "Archivo incorrecto"
			else:
				blob = bucket.blob(folder_path+file.filename)
				blob.upload_from_string(file.filename)
				nueva_imagen = Imagen(
			 		filename = file.filename,
			 		restaurant = restaurante.name,
			 		owner = restaurante.owner
				)
				db.session.add(nueva_imagen)
				db.session.commit()
				return imagen_schema.dump(nueva_imagen)
		else:
			return "El restaurante no existe o usted no es dueño de él"
	
class RecursoArchivo(Resource):
	# Obtener enlace a imagen de restaurante
	@jwt_required()
	def post(self, restaurante_id):
		restaurante = Restaurante.query.filter_by(id=restaurante_id).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
			filename = request.json['file']
			file = Imagen.query.filter_by(filename=filename).first()
			if file:
				return "https://storage.googleapis.com/flask-bucket-app/{}/{}/{}".format(file.owner, file.restaurant, file.filename)
			else:
				return "Archivo inexistente"
		else:
			return "El restaurante no existe o usted no es el dueño de él"

	# Eliminar imagen de restaurante
	@jwt_required()
	def put(self, restaurante_id):
		restaurante = Restaurante.query.filter_by(id=restaurante_id).first()
		if restaurante and restaurante.owner == get_jwt_identity()[0]:
			filename = request.json['file']
			file = Imagen.query.filter_by(filename=filename).first()
			if file:
				folder_path = restaurante.owner + '/' + restaurante.name + '/'
				if storage.Blob(bucket=bucket, name=folder_path+file.filename).exists(client):
					blob = bucket.blob(folder_path+file.filename)
					blob.delete()
					db.session.delete(file)
					db.session.commit()
					return "Archivo removido correctamente"
				else:
					return "El archivo no se encuentra almacenado"
			else:
				return "Archivo inexistente"
		else:
			return "El restaurante no existe o usted no es el dueño de él"

api.add_resource(RecursoRestaurante, '/restaurante')
api.add_resource(RecursoNuevoRestaurante, '/restaurante/nuevo')
api.add_resource(RecursoBorrarRestaurante, '/restaurante/<int:restaurante_id>')

api.add_resource(RecursoRegistro, '/registro')
api.add_resource(RecursoLogin, '/login')

api.add_resource(RecursoArchivo, '/restaurante/<int:restaurante_id>/archivo')
api.add_resource(RecursoNuevoArchivo, '/restaurante/<int:restaurante_id>/archivo/nuevo')

# Execution
if __name__ == '__main__':
	app.run(debug=True)
