import requests
import json
from config import API_BASE

def create_session(username:str, identity:str):
    sess = requests.Session()
    with sess.post(f"{API_BASE}/login", json={"account":username,"identity":identity}) as resp:
        resp.raise_for_status()
    return sess

def default_auth(func):
    def decorator(*args, **kwargs):
        user = json.loads(open("auth/user.json", "r").read())
        sess = create_session(user["account"], user["identity"])
        print(f"args:{type(args)}")
        args = (sess, *args)
        return func(*args, **kwargs)
    return decorator