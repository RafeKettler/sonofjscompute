from flask import Blueprint

tasks = Blueprint('tasks', 'sonofjscompute.views.tasks')

@tasks.route('/', methods=['GET'])
def list_tasks():
    return ''

@tasks.route('/', methods=['POST'])
def create_task():
    return ''
