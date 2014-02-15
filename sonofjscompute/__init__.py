from flask import Flask

from sonofjscompute.views import tasks

def create_app():
    app = Flask(__name__)
    app.config.from_object('sonofjscompute.config')
    
    app.register_blueprint(tasks, url_prefix='/tasks')
    
    return app
