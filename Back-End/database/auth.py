from .schema import (
    User
)
from mongoengine.queryset.visitor import Q

def create_user(account:str, identity:str):
    if len(User.objects(Q(account = account)|Q(identity = identity))) != 0:
        raise ValueError("user name or identity have already taken")
    User(
        account = account,
        identity = identity
    ).save()

def check_user_exist(account:str, identity:str)->bool:
    return len(User.objects(account = account, identity = identity)) == 1