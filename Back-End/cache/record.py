from . import *
import redis
from database.node.devlog import (
    create_device_logs
)
from .dev_map import (
    get_hid
)
from datetime import (
    datetime
)
from pickle import (
    loads,
    dumps
)

RECORD_BUFSZ = 3 # one was reserved for lastest record

def save_cache(node_uuid:str, device_id:str):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    prefix = f"node-{node_uuid}-dev-{device_id}"

    key = f"{prefix}-record"
    ts_key = f"{prefix}-timestamp"

    recs = red.lrange(key, 0, -2) # last key is 0 or previous last record
    recs_ts = red.lrange(ts_key, 0, -2) # last key is 0 or previous last record

    for idx, val in enumerate(recs):
        recs[idx] = {
            "val":val,
            "ts":loads(recs_ts[idx])
        }
    
    create_device_logs(node_uuid, get_hid(node_uuid, device_id), recs)
    red.ltrim(key, 0, 0) # only preserve lastest record
    red.ltrim(ts_key, 0, 0) # only preserve lastest record

def write_cache(record:dict):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    get_hid(record["token"], record['device'])
    prefix = f"node-{record['token']}-dev-{record['device']}"
    key = f"{prefix}-record"

    red.lpushx(key, record['amount'])
    red.lpushx(f"{prefix}-timestamp", dumps(datetime.now()))

    if red.llen(key) >= RECORD_BUFSZ:
        save_cache(record['token'], record['device'])

def get_latest_record(node_uuid:str, hid:str)->float:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    serial_num = red.get(f"dev-{hid}-serial-num")
    if serial_num is None:
        raise IndexError(f"can not get hid {hid} serial num")

    serial_num = serial_num.decode()
    rec = red.lindex(f"node-{node_uuid}-dev-{serial_num}-record", 0)
    if rec is None:
        raise IndexError(f"can not get lasted record of node-{node_uuid}-dev-{serial_num}-record")
    return float(rec.decode())