from flask import Flask

from sonofjscompute.models import create_redis
from sonofjscompute.views import tasks

def create_app():
    app = Flask(__name__)
    app.config.from_object('sonofjscompute.config')
    
    create_redis(app)

    app.register_blueprint(tasks, url_prefix='/tasks')
    
    return app
