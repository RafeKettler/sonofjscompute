from json import dumps
from json import loads

from test import TestCase

class TestTasks(TestCase):
    def test_create_task(self):
        data = { 
            'name' : 'foo',
            'url'  : 'https://s3.amazonaws.com/sonofjscompute-testing/sample.json'
        }
        
        resp = self.client.post('/tasks/', data=data)
        self.assertEquals(201, resp.status_code)
        json = loads(resp.data)
        self.assertTrue(json['id'])
        self.assertEquals('foo', json['name'])
