from pickle import loads
from multiprocessing import Process
from redis import StrictRedis

class Worker(object):
    def __init__(self, queue_name=None, from_queue=None, host='127.0.0.1', port=6379, db=0, prefix='easy_jobs:queue:'):
        self.queue_name = queue_name
        self.from_queue = from_queue
        self.outputs = ['results']

        if from_queue:
            self.connection = self.from_queue.connection
            self.key = self.from_queue.key
        else:
            self.key = '%s%s' % (prefix, queue_name)
            self.connection = StrictRedis(host=host, port=port, db=db)

    def start(self, once=False, threaded=False):
        jobs = self.connection.llen(self.key)

        while jobs > 0:
            pickled = self.connection.rpop(self.key)

            if pickled:
                un_pickled = loads(pickled)
                instance = un_pickled['foo']
                args = un_pickled['args']
                kwargs = un_pickled['kwargs']
                p = Process(target=instance, args=args, kwargs=kwargs)
                p.start()

                if not threaded:
                    p.join()
            jobs = self.connection.llen(self.key) if not once else -1

