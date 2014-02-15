from flask import current_app
from redis import Redis

# Uses a connection pool behind the scenes, is threadsafe, yada yada
redis = Redis(host=current_app.config['REDIS_HOST'], 
              port=current_app.config['REDIS_PORT'])

class Model(object):
    @classmethod
    def create(cls, **attributes):
        model = cls(**attributes)
        model.id = redis.incr('%s_id' % cls.__prefix__)
        model.save()
        return model

    @classmethod
    def get(cls, id):
        model = cls(**attributes)
        model.load()
        return model

class Task(Model):
    __prefix__ = 'tasks'

    def __init__(self, **attributes):
        pass

    def load(self):
        pass

    def save(self):
        pass
