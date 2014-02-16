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
        if len(self.inputs) > 0:
            redis.rpush('%s:requests-queue' % namespace, *self.inputs)

    def remaining_count(self):
        return redis.llen('%s:requests-queue' % self.namespace())

    def get_requests(self):
        return redis.lrange('%s:requests-queue' % self.namespace(), 0, -1)

    def get_results(self):
        return redis.lrange('%s:results-queue' % self.namespace(), 0, -1)

    def get_task_request(self):
        namespace = self.namespace()
        transaction = redis.pipeline()
        transaction.hincrby(namespace, 'processing', 1)
        transaction.lpop('%s:requests-queue' % namespace)
        _, request = transaction.execute()
        return request

    def add_task_result(self, result):
        namespace = self.namespace()
        print result
        transaction = redis.pipeline()
        transaction.hincrby(namespace, 'processing', -1)
        transaction.rpush('%s:results-queue' % namespace, result)
        transaction.execute()

    def get_task_result(self):
        namespace = self.namespace()
        _, result = redis.blpop('%s:results-queue' % namespace)
        return result

    def is_processing(self):
        namespace = self.namespace()
        transaction = redis.pipeline()
        transaction.hget(namespace, 'processing')
        transaction.llen('%s:requests-queue' % namespace)
        processing, requests_len = transaction.execute()
        return requests_len > 0 or (processing and processing != 0)

    def dict(self):
        return dict(id=self.id, name=self.name)
