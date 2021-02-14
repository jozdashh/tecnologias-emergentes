from flask import Flask

# Inits and configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask'
app.secret_key = '#0#'