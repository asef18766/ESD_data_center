import redis
import os
import logging
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
logging.warning(f"REDIS_HOST:{REDIS_HOST}")
REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=0)
redis.StrictRedis(connection_pool=REDIS_POOL).flushall()