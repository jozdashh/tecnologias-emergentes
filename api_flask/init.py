from flask import Flask

# Inits and configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@10.188.64.2/flask'
app.secret_key = '#0#'
