import unittest

from sonofjscompute import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        from sonofjscompute import models
        self.app = create_app()
        self.client = self.app.test_client()
        models.create_redis(self.app, db=1)
        self.redis = models.redis
        self.addCleanup(self._teardown_redis)

    def _teardown_redis(self):
        self.redis.flushdb()
