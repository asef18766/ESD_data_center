import requests
from config import API_BASE

def create_session(username:str, identity:str):
    sess = requests.Session()
    with sess.post(f"{API_BASE}/login", json={"account":username,"identity":identity}) as resp:
        resp.raise_for_status()
    return sess