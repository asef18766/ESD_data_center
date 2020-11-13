from random import getrandbits
from ..schema import (
    FarmNode
)

def create_node(node_name:str = "my farm")->str:
    token = hex(getrandbits(64))[2:]
    farm_node = FarmNode(
        token = token,
        node_name = node_name
    ).save()
    return token

def get_node_instance(node_token:str)->FarmNode:
    node = FarmNode.objects(token=node_token).get()
    if node == None:
        raise IndexError(f"can not found node with token {node_token}")
    return node

# WIP
def update_node(
    node_token:str,
    node_name:str,
    icon_link:str,
    input_devices:list,
    output_devices:list
):
    pass
    node = get_node_instance(node_token)
    if node_name != None:
        node.node_name = node_name
    if icon_link != None:
        node.icon_link = icon_link
    if input_devices != None:
        for dev in input_devices:
            node.input_devices((dev["name"]))
