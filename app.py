from flask_sockets import Sockets, log_request
from json import dumps

from sonofjscompute import create_app
from sonofjscompute.models import Task


app = create_app()
sockets = Sockets(app)

@sockets.route('/mosaic/')
def echo_socket(ws):
    ws.receive()
    task = Task.get_last()
    while task.is_processing():
        result = task.get_task_result()
        ws.send(dumps({'url':result}))
    ws.close()
