from . import *
import redis

def create_map(node_uuid:str, devices:list)->dict:
    '''
    return a map which maps hid to an interger for a single node
    '''
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    maps = {}
    for i in range(len(devices)):
        # create map caches
        if not red.set(f"node-{node_uuid}-dev-{i}", devices[i]):
            raise Exception(f"unable to write mapping on node_uuid {node_uuid}")
        if not red.set(f"dev-{devices[i]}-serial-num", i):
            raise Exception(f"unable to write reverse serial num mapping on node_uuid {node_uuid}")
        if not red.set(f"dev-{devices[i]}-node", node_uuid):
            raise Exception(f"unable to write reverse device mapping on node_uuid {node_uuid}")

        maps.update({devices[i]:i})
        red.lpush(f"node-{node_uuid}-dev-{i}-record",0)
    return maps

def get_hid(node_uuid:str, dev_serial_num:int)->str:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    hid:bytes=red.get(f"node-{node_uuid}-dev-{dev_serial_num}")
    if hid is None:
        raise IndexError(f"can not get hid from node-{node_uuid}-{dev_serial_num}")
    hid = hid.decode()
    
    return hid

def get_device_owner(hid:str)->str:
    red = redis.StrictRedis(connection_pool=REDIS_POOL)
    node_id:bytes = red.get(f"dev-{hid}-node")
    if node_id is None:
        raise IndexError(f"can not get node id from hid {hid}")
    return node_id.decode()
