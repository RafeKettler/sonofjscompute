from json import dumps
from json import loads

from sonofjscompute.models import Task

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
        inputs = Task.get(json['id']).get_requests()
        self.assertEquals(2, len(inputs))
        self.assertEquals('foo', inputs[0])
        self.assertEquals('bar', inputs[1])
