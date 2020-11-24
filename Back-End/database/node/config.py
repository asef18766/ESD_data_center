from random import getrandbits

from .node import get_node_instance
from ..schema import (
    FarmNode,
    NodeConfig,
    User
)

def config_deserializer(node_cfg:NodeConfig)->dict:
    res = node_cfg.to_mongo().to_dict()
    res.pop("_id")
    return res

# TODO: add checking when serialization
def config_serializer(cfg:dict)->NodeConfig:
    return NodeConfig(**cfg).save()

def get_node_config(node_token:str)->NodeConfig:
    node = get_node_instance(node_token)
    cfg = config_deserializer(node.config)
    inputs = node.input_devices
    outputs = node.output_devices
    cfg.update({
        "input_devices":inputs,
        "output_devices":outputs
    })
    return cfg

def update_node_config(node_token:str, user_config:dict):
    node:FarmNode = get_node_instance(node_token)
    if node is None:
        raise IndexError(f"can not found node {node_token}")
    lst_ver:int = node.config.version
    print(f"lst ver:{lst_ver}")
    lst_ver += 1
    user_config.update({"version":lst_ver})
    node.config = config_serializer(user_config)
    node.save()