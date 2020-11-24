from random import getrandbits
from .node import get_node_instance
from ..schema import (
    FarmNode,
    User,
    NodeConfig
)
def get_user_instance(user_id:str)->User:
    user = User.objects(identity = user_id).get()
    if user == None:
        raise IndexError(f"can not found user {user_id}")
    return user

def assign_node_owner(node_token:str, user_id:str):
    node = get_node_instance(node_token)
    user = get_user_instance(user_id)
    if node in user.nodes:
        raise ValueError(f"node already exist {node_token}")
    user.nodes.append(node)
    user.save()

def list_user_node(user_id:str)->list:
    user = get_user_instance(user_id)
    nodes = [str(n.id) for n in user.nodes]
    return nodes

def user_has_node(user_id:str, node_id:str)->bool:
    return node_id in list_user_node(user_id)

def check_node_owner(user_id:str, node_ids:list)->list:
    '''
    check wheather the nodes belong to user
    '''
    nodes = list_user_node(user_id)
    if "*" in node_ids:
        return nodes
    
    for nid in node_ids:
        if nid not in nodes:
            raise IndexError(f"{nid} does not belongs to user")

    return node_ids
