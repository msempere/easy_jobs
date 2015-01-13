from unittest import TestCase
from easy_jobs import Queue, Worker
from time import sleep
from aux import foo

class TestQueue(TestCase):
    def test_empty_queue(self):
        queue = Queue('test_1')
        assert 0 == len(queue)

    def test_inserting_element(self):
        queue = Queue('test_2')
        queue.push(foo, 1)
        assert 1 == len(queue)

    def test_timeout_queue(self):
        queue = Queue('test_3')
        queue.push(foo, 1, timeout=1)
        assert 1 == len(queue)
        sleep(1)
        assert 0 == len(queue)

    def test_consuming(self):
        queue = Queue('test_3')
        worker = Worker(queue_name='test_3')
        queue.push(foo, 10)
        queue.push(foo, 10)
        assert 2 == len(queue)
        worker.start(once=True)
        assert 1 == len(queue)
        worker.start(once=True)
        assert 0 == len(queue)
