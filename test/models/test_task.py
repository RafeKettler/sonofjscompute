from redis import Redis
from test import TestCase

from sonofjscompute import models
from sonofjscompute.models import Task

class TestTask(TestCase):
    def setUp(self):
        super(TestTask, self).setUp()
        models.create_redis(self.app, db=1)
        self.addCleanup(self._teardown_redis)

    def test_create_and_get_task(self):
        task = Task.create(name='foo', inputs=['foo','bar'])
        self.assertEquals('foo', task.name)
        self.assertEquals(2, len(task.inputs))
        self.assertFalse(task.is_processing())
        self.assertTrue(task.has_requests())

        gotten = Task.get(task.id)
        self.assertEquals('foo', gotten.name)
        self.assertEquals(2, len(gotten.inputs))
        self.assertFalse(task.is_processing())
        self.assertTrue(gotten.has_requests())

    def test_get_task_request(self):
        task = Task.create(name='foo', inputs=['foo', 'bar'])
        self.assertEquals(2,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertFalse(task.is_processing())
        self.assertTrue(task.has_requests())

        request = task.get_task_request()
        self.assertEquals('foo', request)
        self.assertTrue(task.is_processing())

        self.assertEquals(1,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertEquals('1',
            models.redis.hget('tasks:%d' % task.id, 'processing'))
        self.assertTrue(task.has_requests())

        request = task.get_task_request()
        self.assertEquals('bar', request)
        self.assertTrue(task.is_processing())

        self.assertEquals(0,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertEquals('2',
            models.redis.hget('tasks:%d' % task.id, 'processing'))
        self.assertFalse(task.has_requests())

    def test_add_and_get_task_result(self):
        task = Task.create(name='foo', inputs=['foo', 'bar'])
        self.assertEquals(2,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertFalse(task.is_processing())

        task.add_task_result('baz')
        self.assertEquals(2,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertEquals(1,
            models.redis.llen('tasks:%d:results-queue' % task.id))
        self.assertEquals('-1',
            models.redis.hget('tasks:%d' % task.id, 'processing'))
        self.assertTrue(task.has_requests())

        result = task.get_task_result()
        self.assertEquals('baz', result)
        self.assertEquals(2,
            models.redis.llen('tasks:%d:requests-queue' % task.id))
        self.assertEquals(0,
            models.redis.llen('tasks:%d:results-queue' % task.id))
        self.assertEquals('-1',
            models.redis.hget('tasks:%d' % task.id, 'processing'))
        self.assertTrue(task.has_requests())

    def _teardown_redis(self):
        models.redis.flushdb()
