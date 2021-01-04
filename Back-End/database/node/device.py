from .node import (
    get_node_instance
)
from .user import (
    get_user_instance
)
from ..schema import (
    DeviceMeta,
    FarmNode
)
from mongoengine.errors import (
    DoesNotExist
)
def get_device_instance(hid:str)->DeviceMeta:
    try:
        dev = DeviceMeta.objects(hid = hid).get()
    except DoesNotExist:
        raise IndexError(f"can not found device with hid {hid}")

    if dev is None:
        raise IndexError(f"can not found device with hid {hid}")
    return dev

def dev_meta_2_dict(devmeta:DeviceMeta)->dict:
    res:dict = devmeta.to_mongo().to_dict()
    res.pop("_id")
    return res

def register_devices(node_token:str, i_devs:list, o_devs:list)->(list, list):
    node = get_node_instance(node_token)
    
    i_dev_list = []
    o_dev_list = []

    for i_d in i_devs:
        try:
            i_dev_list.append(get_device_instance(i_d["hid"]))
        except IndexError:
            i_dev_list.append(DeviceMeta(
                hid = i_d["hid"],
                name = i_d["name"],
                worker_type = True,
                min_throughput = i_d["min_input"],
                max_throughput = i_d["max_input"],
                unit = i_d["unit"]
            ).save())
    
    for o_d in o_devs:
        try:
            o_dev_list.append(get_device_instance(o_d["hid"]))
        except IndexError:
            o_dev_list.append(DeviceMeta(
                hid = o_d["hid"],
                name = o_d["name"],
                worker_type = False,
                min_throughput = o_d["min_output"],
                max_throughput = o_d["max_output"],
                unit = o_d["unit"]
            ).save())
    node.input_devices = i_dev_list
    node.output_devices = o_dev_list
    node.save()

    i_dev_list = [i.id for i in i_dev_list]
    o_dev_list = [i.id for i in o_dev_list]
    
    return (i_dev_list, o_dev_list)

def dev_name_2_hid(nodes:list, dev_names:list)->(dict, dict):
    '''
    return a dictionary key defined as device name,
    value as a list of hids
    '''
    res = {}
    pic_url = {}
    for k in dev_names:
        res.update({k:[]})
        pic_url.update({k:""})

    for node in nodes:
        node = get_node_instance(node)
        dev_icons = node.config.device_icons
        hid = None
        for dm in node.input_devices:
            if dm.name in dev_names:
                res[dm.name].append(dm.hid)
                if dm.hid not in dev_icons:
                    continue
                url = dev_icons[dm.hid]
                if url != None and url != "":
                    pic_url[dm.name] = dev_icons[dm.hid]
        
        for dm in node.output_devices:
            if dm.name in dev_names:
                res[dm.name].append(dm.hid)
                if dm.hid not in dev_icons:
                    continue
                url = dev_icons[dm.hid]
                if url != None and url != "":
                    pic_url[dm.name] = dev_icons[dm.hid]
    
    for k,v in res.items():
        if v == []:
            raise IndexError(f"device name {k}")
    
    return res, pic_url