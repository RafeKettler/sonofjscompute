from flask.ext.script import Manager
import json
import multiprocessing
import os
from PIL import Image
import requests
from StringIO import StringIO

from app import app
from sonofjscompute import models
from sonofjscompute.models import Task
from sonofjscompute.workers import PixelWorker
from sonofjscompute.workers import Worker

manager = Manager(app)

def _work(task):
    Worker(task).work()

def _work_mosaic(task):
    PixelWorker(task).work()

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

RESOLUTION = 60
    
@manager.command
def start_mosaic(url='http://25.media.tumblr.com/tumblr_mb50xf8S9c1rgw39go1_500.jpg'):
    response = requests.get(url)
    image = Image.open(StringIO(response.content))
    width, height = image.size
    inputs = []
    for x in range(0, width, RESOLUTION):
        for y in xrange(0, height, RESOLUTION):
            tile = image.crop(box=(x, y, x + RESOLUTION, y + RESOLUTION))
            r = g = b = 0.0
            for pixel in tile.getdata():
                try:
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]
                except IndexError:
                    r += pixel
                    g += pixel
                    b += pixel
            num_pixels = float(len(tile.getdata()))
            r,g,b = r/num_pixels, g/num_pixels, b/num_pixels
            inputs.append(json.dumps({'x':x, 'y':y, 'r':r, 'g':g, 'b':b}))

    models.create_redis(app, db=2)
    task = Task.create(name='mosaic', inputs=inputs)
    processes = multiprocessing.cpu_count() or 1
    pool = multiprocessing.Pool(processes)
    pool.map(_work_mosaic, [task] * processes)
    
if __name__ == '__main__':
    manager.run()
