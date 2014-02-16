from sonofjscompute import create_app
from flask_sockets import Sockets, log_request
from sonofjscompute.models import redis

app = create_app()
sockets = Sockets(app)

@sockets.route('/create_task/')
def echo_socket(ws):
    task_id = ws.receive()
    task = Task.get(task_id)
    while task.has_requests() and task.is_processing():
      result = task.blpop()
      ws.send(message)
    ws.close()
