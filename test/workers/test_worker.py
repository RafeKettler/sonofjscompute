from test import TestCase

from sonofjscompute.models import Task
from sonofjscompute.workers import Worker

class TestWorker(TestCase):
    def test_worker_no_requests(self):
        task = Task.create(name='foo', inputs=[])
        worker = Worker(task)
        worker.work()
        
        self.assertEquals(0, len(task.get_requests()))
        self.assertEquals(0, len(task.get_results()))

    def test_worker_some_requests(self):
        task = Task.create(name='foo', inputs=['foo', 'bar'])
        worker = Worker(task)
        worker.work()
        
        self.assertEquals(0, len(task.get_requests()))
        results = task.get_results()
        self.assertEquals(2, len(results))
        self.assertIn('foo', results)
        self.assertIn('bar', results)

