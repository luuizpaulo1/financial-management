from flask import Flask
from sql_alchemy import db
from api import setup_blueprint as blueprint
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# default='postgresql://postgres:123456789@localhost:5432/postgres')

db.init_app(app)

app.register_blueprint(blueprint(app))

if __name__ == '__main__':
    app.run(debug=True)
