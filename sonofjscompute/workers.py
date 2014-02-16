from multiprocessing import Pool

from sonofjscompute import models

class Worker(object):
    def __init__(self, task):
        self.task = task

    def work(self):
        while self.task.remaining_count() > 0:
            input = self.task.get_task_request()
            self.task.add_task_result(self.run(input))

    def run(self, input):
        return input
