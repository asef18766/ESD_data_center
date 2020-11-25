from . import *
import redis
from database.node.devlog import (
    create_device_logs
)
from .dev_map import (
    get_hid
)

RECORD_BUFSZ = 3

def save_cache(node_uuid:str, device_id:str):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    key = f"node-{node_uuid}-dev-{device_id}-record"
    recs = red.lrange(key, 0, 1)
    create_device_logs(node_uuid, get_hid(node_uuid, device_id), recs)
    red.ltrim(key, 0, 1)

def write_cache(record:dict):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    get_hid(record["token"], record['device'])
    key = f"node-{record['token']}-dev-{record['device']}-record"

    red.lpushx(key, record['amount'])
    if red.llen(key) >= RECORD_BUFSZ:
        save_cache(record['token'], record['device'])

def get_latest_record(node_uuid:str, hid:str)->float:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    serial_num = red.get(f"dev-{hid}-serial-num")
    if serial_num is None:
        raise IndexError(f"can not get hid {hid} serial num")

    rec = red.lindex(f"node-{node_uuid}-dev-{serial_num}-record", -1)
    if rec is None:
        raise IndexError(f"can not get lasted record of node-{node_uuid}-dev-{serial_num}-record")
    return rec