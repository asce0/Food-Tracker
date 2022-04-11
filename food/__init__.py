from doctest import FAIL_FAST
import imp
from flask import Flask
from .app.routes import main
from .extensions import db


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main)
  
    return app