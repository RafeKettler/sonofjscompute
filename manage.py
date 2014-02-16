from flask.ext.script import Manager
import multiprocessing
import os

from app import app
from sonofjscompute.models import Task
from sonofjscompute.workers import Worker

manager = Manager(app)

def _work(task_id):
    Worker(Task.get(task_id)).work()

@manager.command
def run_worker(task_id):
    task_id = int(task_id)
    processes = multiprocessing.cpu_count() or 1
    pool = multiprocessing.Pool(processes)
    pool.map(_work, [task_id] * processes)

if __name__ == '__main__':
    manager.run()
