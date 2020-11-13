from random import getrandbits
from .node import get_node_instance
from ..schema import (
    FarmNode,
    User
)

def assign_node_owner(node_token:str, user_id:str):
    node = get_node_instance(node_token)
    user = User.objects(identity = user_id).get()
    if user == None:
        raise IndexError(f"can not found user {user_id}")
    print(user)
    user.nodes.append(node)
    user.save()
