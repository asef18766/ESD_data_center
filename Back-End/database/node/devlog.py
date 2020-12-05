from .node import (
    get_node_instance
)
from .device import (
    get_device_instance
)
from ..schema import (
    DeviceLog
)
from datetime import (
    datetime
)
from mongoengine import (
    Q
)

def create_device_logs(node_token:str, device_id:str, logs:list):
    node = get_node_instance(node_token)
    device = get_device_instance(device_id)

    log_collection = [ DeviceLog(owner=node, device = device, data = log["val"], timestamp= log["ts"])  for log in logs]
    DeviceLog.objects.insert(log_collection)
    node.update(push_all__dev_logs=log_collection)

def get_all_dev_log(node_tokens:list, dev_ids:list, ts_start:datetime, ts_end:datetime, limit_count:int):
    node_filters = Q()
    device_filters = Q()
    date_filters = Q()

    for nt in node_tokens:
        node_filters = node_filters | Q(owner=get_node_instance(nt))

    for hid in dev_ids:
        device_filters = device_filters | Q(device=hid)
    
    if ts_start is not None:
        date_filters = date_filters & Q(timestamp__gte=ts_start)
    if ts_end is not None:
        date_filters = date_filters & Q(timestamp__lte=ts_end)
    print(f"node_filters:{node_filters}")
    print(f"device_filters:{device_filters}")
    print(f"date_filters:{date_filters}")
    
    return DeviceLog.objects( (node_filters) & (device_filters) & (date_filters))[:limit_count].as_pymongo()

    
