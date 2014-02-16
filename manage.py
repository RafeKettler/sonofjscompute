from flask.ext.script import Manager
import multiprocessing
import os

from app import app
from sonofjscompute import models
from sonofjscompute.models import Task
from sonofjscompute.workers import Worker

manager = Manager(app)

def _work(task):
    Worker(task).work()

@manager.command
def run_worker(task_id):
    task_id = int(task_id)
    task = Task.get(task_id)
    processes = multiprocessing.cpu_count() or 1
    pool = multiprocessing.Pool(processes)
    pool.map(_work, [task] * processes)

@manager.command
def aww():
    t = Task.create(name='test', inputs=[
        'http://i.imgur.com/zOEilgl.jpg',
        'http://i.imgur.com/wDRinK6.jpg',
        'http://i.imgur.com/f5uhRgN.jpg', 
        'http://i.imgur.com/xSgkwpO.jpg?1'])
    processes = multiprocessing.cpu_count() or 1
    pool = multiprocessing.Pool(processes)
    pool.map(_work, [t] * processes)

if __name__ == '__main__':
    manager.run()
