import json
from multiprocessing import Pool
from time import sleep

from sonofjscompute import models

class Worker(object):
    def __init__(self, task):
        self.task = task

    def work(self):
        while self.task.remaining_count() > 0:
            input = self.task.get_task_request()
            if input is not None:
                self.task.add_task_result(self.run(input))

    def run(self, input):
        return input

class PixelWorker(Worker):
    def __init__(self, task):
        self.images = None
        super(PixelWorker, self).__init__(task)
    
    def _distance(self, a, b):
        r1, g1, b1 = a
        r2, g2, b2 = b
        return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
    
    def run(self, input):
        input = json.loads(input)
        color = (input['r'], input['g'], input['b'])
        if self.images is None:
            self.images = [json.loads(photo) for photo in
                           models.redis.lrange('photos', 0, -1)]
        best_match = None
        best_distance = None
        for image in self.images:
            distance = self._distance(color, (image['r'], image['g'], image['b']))
            if best_distance is None or best_distance > distance:
                best_distance = distance
                best_match = image
        data = {
            'x':input['x'],
            'y':input['y'],
            'url':best_match['url']
        }
        return json.dumps(data)
