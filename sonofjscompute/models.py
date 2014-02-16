from flask import current_app
from json import dumps
from redis import Redis

def create_redis(app, **kwargs):
    global redis
    redis = Redis(host=app.config['REDIS_HOST'],
                  port=app.config['REDIS_PORT'],
                  **kwargs)

class Model(object):
    @classmethod
    def create(cls, **attributes):
        model = cls(**attributes)
        model.id = redis.incr('%s_id' % cls.__prefix__)
        model.save()
        return model

    @classmethod
    def get(cls, id):
        model = cls()
        model.id = id
        model.load()
        return model

    def dict(self):
        return {}

    def namespace(self):
        return '%s:%d' % (self.__prefix__, self.id)

class Task(Model):
    __prefix__ = 'tasks'

    def __init__(self, **attributes):
        self.name = attributes.get('name')
        self.inputs = attributes.get('inputs')

    def load(self):
        namespace = self.namespace()
        self.name = redis.hget(namespace, 'name')
        self.inputs = redis.lrange('%s:requests-queue' % namespace, 0, -1) + \
            redis.lrange('%s:results-queue' % namespace, 0, -1)

    def save(self):
        namespace = self.namespace()
        redis.hset(namespace, 'name', self.name)
        redis.rpush('%s:requests-queue' % namespace, *self.inputs)

    def get_task_request(self):
        namespace = self.namespace()
        redis.hincrby(namespace, 'processing', 1)
        return redis.lpop('%s:requests-queue' % namespace)

    def add_task_result(self, result):
        namespace = self.namespace()
        print namespace
        redis.hincrby(namespace, 'processing', -1)
        redis.rpush('%s:results-queue' % namespace, result)

    def get_task_result(self):
        namespace = self.namespace()
        return redis.lpop('%s:results-queue' % namespace)

    def is_processing(self):
        namespace = self.namespace()
        processing = redis.hget(namespace, 'processing')
        return processing and processing != 0

    def has_requests(self):
        return redis.llen('%s:requests-queue' % self.namespace()) > 0

    def dict(self):
        return dict(id=self.id, name=self.name)
