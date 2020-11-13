from random import getrandbits

from .node import get_node_instance
from ..schema import (
    FarmNode,
    NodeConfig,
    User
)

def get_node_config(node_token:str)->NodeConfig:
    node = get_node_instance(node_token)
    cfg = NodeConfig.objests(node = node).get()
    
    # if configure not exsist, create one
    if cfg == None:
        cfg = NodeConfig(node=node, version=0)
    return cfg