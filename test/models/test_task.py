from redis import Redis
from test import TestCase

from sonofjscompute import models
from sonofjscompute.models import Task

class TestTask(TestCase):
    def test_create_and_get_task(self):
        task = Task.create(name='foo', inputs=['foo','bar'])
        self.assertEquals('foo', task.name)
        self.assertEquals(2, len(task.inputs))
        self.assertTrue(task.is_processing())

        gotten = Task.get(task.id)
        self.assertEquals('foo', gotten.name)
        self.assertEquals(2, len(gotten.inputs))
        self.assertTrue(task.is_processing())

    def test_remaining_count(self):
        task = Task.create(name='foo', inputs=[])
        self.assertEquals(0, task.remaining_count())

        task = Task.create(name='foo', inputs=['foo','bar'])
        self.assertEquals(2, task.remaining_count())

    def test_get_task_request(self):
        task = Task.create(name='foo', inputs=['foo', 'bar'])
        self.assertEquals(2, len(task.get_requests()))
        self.assertTrue(task.is_processing())

        request = task.get_task_request()
        self.assertEquals('foo', request)
        self.assertTrue(task.is_processing())

        self.assertEquals(1,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertEquals('1', 
            self.redis.hget('tasks:%d' % task.id, 'processing'))
        self.assertTrue(task.is_processing())
        self.assertEquals(1, len(task.get_requests()))

        request = task.get_task_request()
        self.assertEquals('bar', request)
        self.assertTrue(task.is_processing())
        self.assertEquals(0, len(task.get_requests()))

    def test_add_and_get_task_result(self):
        task = Task.create(name='foo', inputs=['foo', 'bar'])
        self.assertEquals(2, len(task.get_requests()))

        task.add_task_result('baz')
        self.assertEquals(2, len(task.get_requests()))
        self.assertEquals(1, len(task.get_results()))
        self.assertEquals('-1',
            self.redis.hget('tasks:%d' % task.id, 'processing'))

        result = task.get_task_result()
        self.assertEquals('baz', result)
        self.assertEquals(2, len(task.get_requests()))
        self.assertEquals(0, len(task.get_results()))
        self.assertEquals('-1',
            self.redis.hget('tasks:%d' % task.id, 'processing'))
