from flask import Flask

from sonofjscompute.views import tasks

app = Flask('sonofjscompute')
app.config.from_object('sonofjscompute.config')
app.register_blueprint(tasks, url_prefix='/tasks')
