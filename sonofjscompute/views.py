from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from json import loads
import requests
import wtforms as wtf

from flask_sockets import Sockets

from sonofjscompute.models import Task

def created(model):
    return jsonify(model.dict()), 201

def error(errors):
    return jsonify(errors), 400

tasks = Blueprint('tasks', 'sonofjscompute.views.tasks')

class TaskForm(wtf.Form):
    name = wtf.StringField('name', [wtf.validators.InputRequired()])
    url  = wtf.StringField('url', [wtf.validators.InputRequired(),
                                   wtf.validators.URL()])

@tasks.route('/', methods=['POST'])
def create_task():
    form = TaskForm(request.form)
    if not form.validate():
        return error(form.errors)
    response = requests.get(form.url.data)
    task = Task.create(name=form.name.data, inputs=response.json())
    return created(task)
