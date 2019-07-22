from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from config import app_config
from .response import InvalidUsage

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models

    from .mental_models import mental_models
    app.register_blueprint(mental_models)

    @app.route('/')
    def hello_world():
        return jsonify(['hello', 'world'])

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
