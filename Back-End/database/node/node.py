from random import getrandbits
from ..schema import (
    FarmNode,
    NodeConfig
)

def create_node(node_name:str = "my farm")->str:
    '''
    create an farm node & assign empty config
    '''
    token = hex(getrandbits(64))[2:]
    config = NodeConfig(
        version = 0,
        node_name = node_name
    ).save()
    farm_node = FarmNode(
        token = token,
        config = config
    ).save()
    return token

def get_node_instance(node_token:str)->FarmNode:
    node = FarmNode.objects(token=node_token).get()
    if node == None:
        raise IndexError(f"can not found node with token {node_token}")
    return node

