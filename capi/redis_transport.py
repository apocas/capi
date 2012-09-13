import datetime
import os
import redis
import urlparse

import capi.transport

class RedisTransport(capi.transport.Transport):

    def __init__(self, args):
        super(RedisTransport, self).__init__()
        redis_url = args.host
        _url = urlparse.urlparse(redis_url, scheme="redis")
        _, _, _db = _url.path.rpartition("/")


        self.redis = redis.StrictRedis(host=_url.hostname, port=_url.port, db=int(_db), socket_timeout=10)
        self.redis_namespace = args.key

    def callback(self, filename, lines):
        timestamp = datetime.datetime.now().isoformat()

        for line in lines:
            if len(line) > 20:
                aux = self.redis.lpush(
                    self.redis_namespace,
                    self.format(filename, timestamp, line)
                )

