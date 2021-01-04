from . import (
    REDIS_POOL
)
from database.node.config import get_node_config
from json import (
    loads,
    dumps
)
import redis

def get_lastest_cfg_ver(node_id:str)->int:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    ver = red.get(f"node-cfg-ver-{node_id}")
    if ver is None:
        raise IndexError(f"can not obtain config version of {node_id}")
    return ver

def get_lastest_cfg(node_id:str)->dict:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    cfg = red.get(f"node-cfg-{node_id}")
    if cfg is None:
        raise IndexError(f"can not obtain config of {node_id}")
    return loads(cfg)

def load_lastest_node_cfg(node_id:str):
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    cfg = get_node_config(node_id)
    red.set(f"node-cfg-{node_id}",dumps(cfg["configures"]))
    red.set(f"node-cfg-ver-{node_id}", cfg["version"])