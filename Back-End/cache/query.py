from . import (
    REDIS_POOL
)
from .record import (
    get_latest_record
)
from .dev_map import (
    get_device_owner
)
from pickle import (
    loads,
    dumps
)
import redis


def get_user_prefer(user_id:str)->dict:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    prefix = f"user-query-{user_id}"
    user_pref:bytes = red.get(f"{prefix}-web-page-map")
    if user_pref is None:
        raise IndexError(f"can not obtain preference of user {user_id}")
    return dumps(user_pref)

def set_user_query_prefer(user_id:str, hids:list, group:str, fe_required_info:dict):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    prefix = f"user-query-{user_id}"

    # query target
    if red.llen(f"{prefix}-hids") != 0:
        red.delete(f"{prefix}-hids")
    red.lpush(f"{prefix}-hids", *hids)

    # proccess method
    red.set(f"{prefix}-group", group)

    # fe required info
    red.set(f"{prefix}-web-page-map", dumps(fe_required_info))
    

def execute_query(user_id:str)->dict:
    '''
    return a dict with {hid : latest value}
    '''
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    prefix = f"user-query-{user_id}"
    hids = red.lrange(f"{prefix}-hids", 0, -1)
    res = {}
    for hid in hids:
        node_id = get_device_owner(hid)
        rec = get_latest_record(node_id, hid)
        # TODO: configure comparison
        res.update({hid:rec})
        
    return res