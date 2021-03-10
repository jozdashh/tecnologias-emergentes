from flask import Flask

# Inits and configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.secret_key = '#0#'
