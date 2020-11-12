from random import getrandbits
from .schema import (
    FarmNode,
    User
)

def create_node(node_name:str = "my farm")->str:
    token = hex(getrandbits(64))[2:]
    farm_node = FarmNode(
        token = token,
        node_name = node_name
    ).save()
    return token

def assign_node_owner(node_token:str, user_id:str):
    node = FarmNode.objects(token=node_token).get()
    if node == None:
        raise IndexError(f"can not found token {node_token}")
    user = User.objects(identity = user_id).get()
    if user == None:
        raise IndexError(f"can not found user {user_id}")
    print(user)
    user.nodes.append(node)
    user.save()

def get_user_nodes(node_token:str):
    pass