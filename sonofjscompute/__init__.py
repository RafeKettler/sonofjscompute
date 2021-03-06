from flask import Flask
from flask_sockets import Sockets
from os import path

from sonofjscompute.models import create_redis
from sonofjscompute.views import tasks

def create_app():
    static_path = path.join(path.dirname(__file__), '../static')
    app = Flask(__name__, static_folder=static_path)
    app.config.from_object('sonofjscompute.config')

    create_redis(app, db=2)
    sockets = Sockets(app)

    app.register_blueprint(tasks, url_prefix='/tasks')

    return app
