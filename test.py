# import os
# import redis
# host = '42.96.132.158'
# psd = 'wjdh84928399'
# r = redis.Redis(host=host, password=psd, db=0, port=6379, socket_timeout=10)
# url = r.lpop('urls')
# f = open('Xspider/payload.txt', 'r')
# list = []
# for line in f.readlines():
#     line = line.strip('\n')
#     url = url + line
#     list.append(url)
# print list

from redlock import Redlock
from redlock import MultipleRedlockException
import time
dlm = Redlock([{"host": "42.96.132.158", "port": 6379, "db": 0, 'password': "wjdh84928399"}, ])

try:
    dlm.servers[0].flushall()
    my_lock = dlm.lock('LOCK', 1000)
    while True:
        if isinstance(my_lock, bool):
            print 'wait'
            time.sleep(0.5)
        else:
            print 'dosomething'
            dlm.servers[0].lpush('urls', time.time())
    dlm.unlock(my_lock)
    time.sleep(0.5)
except MultipleRedlockException, e:
    raise e