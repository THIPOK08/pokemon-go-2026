import os
from flask import Flask
from pokemon.extensions import db, login_manager, bcrypt
from pokemon.models import User, Type, Pokemon
from pokemon.core.routes import core_bp

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  app.register_blueprint(core_bp, url_prefix='/')
  
  return app