# -*- coding:utf-8 -*-

from redis import StrictRedis
try:
    from sparta.sparta_config import REDIS
except ImportError:
    from sparta.setting import REDIS


class RedisBroker(object):

    def __init__(self, **redis_c):
        self.ip_set_name = redis_c.pop('ip_set_name')
        self._r = StrictRedis(**redis_c)

    def ip_notebook(self, ip):
        (count, status) = self._r.hmget(ip, 'count', 'status')
        print count, status
        if not count:
            self._r.hmset(ip, {'count': 1, 'status': 0})
            self._r.sadd(self.ip_set_name, ip)
        else:
            self._r.hincrby(ip, 'count', amount=1)


Redis = RedisBroker(**REDIS)
