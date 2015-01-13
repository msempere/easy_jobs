# easy_jobs
Persistent job queue employing Redis

## Versions:
* master [![Build Status](https://travis-ci.org/msempere/easy_jobs.svg?branch=master)](https://travis-ci.org/msempere/easy_jobs) [![Requirements Status](https://requires.io/github/msempere/easy_jobs/requirements.svg?branch=master)](https://requires.io/github/msempere/easy_jobs/requirements/?branch=master)

## Setup:
```
pip install -r requirements.txt
```
```
python setup.py install
```

## Usage:

```python
from easy_jobs import Queue, Worker

queue = Queue('testing_queue', default_timeout=60)

def foo():
  print time()
  sleep(1)

queue.push(foo, timeout=10) # after the timeout has expired, the job will automatically be deleted
queue.push(foo) # if timeout is not set, 'default_timeout' is used
queue.push(foo, timeout=10)

worker = Worker(queue_name='testing_queue')
worker.start(threaded=False)
# 1421191702.35
# 1421191703.36
# 1421191704.37
```

## Threaded:
Jobs are executed without waiting for the prior to finish
```python
worker = Worker(queue_name='testing_queue')
worker.start(threaded=True)
# 1421191702.35
# 1421191702.35
# 1421191702.35
```

## Step by step executions:
Workers will execute only one job
```python
worker = Worker(queue_name='testing_queue')
worker.start(once=True)
# 1421191702.35
```
