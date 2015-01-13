from pickle import dumps, HIGHEST_PROTOCOL
from worker import Worker
import redis
from time import time, sleep

class Queue(object):

    def __init__(self, name, host='127.0.0.1', port=6379, db=0, default_timeout=120, prefix='easy_jobs:queue:'):
        assert type(name) == str
        assert type(host) == str
        assert type(prefix) == str
        assert type(port) == int
        assert type(db) == int
        assert type(default_timeout) == int

        self.name = name
        self.host = host
        self.port = port
        self.db = db
        self.default_timeout = default_timeout
        self.prefix = prefix
        self.key = '%s%s' % (prefix, name)
        self.connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def __len__(self):
        return self.connection.llen(self.key)

    def push(self, foo, *args, **kwargs):
        timeout = kwargs.pop('timeout', self.default_timeout)
        self.push_foo(foo=foo, args=args, kwargs=kwargs, timeout=timeout)

    def push_foo(self, foo, timeout, args=None, kwargs=None):
        to_pickle = {}
        to_pickle['foo'] = foo
        to_pickle['args'] = args
        to_pickle['kwargs'] = kwargs
        pickled = dumps(to_pickle, protocol=HIGHEST_PROTOCOL)

        with self.connection.pipeline() as pipe:
            pipe.lpush(self.key, pickled)
            pipe.expire(self.key, timeout)
            pipe.execute()

