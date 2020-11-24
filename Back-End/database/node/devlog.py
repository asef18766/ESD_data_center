from .node import (
    get_node_instance
)
from .device import (
    get_device_instance
)
from ..schema import (
    DeviceLog
)
def create_device_logs(node_token:str, device_id:str, logs:list):
    node = get_node_instance(node_token)
    device = get_device_instance(device_id)

    log_collection = [ DeviceLog(device = device, data = log)  for log in logs]
    DeviceLog.objects.insert(log_collection)
    node.update(push_all__dev_logs=log_collection)
    
