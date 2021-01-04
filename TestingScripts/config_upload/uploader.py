from requests import Session
from config import API_BASE
from auth import default_auth

@default_auth
def upload_cfg(sess:Session, node_id:str, cfg:dict):
    with sess.post(f"{API_BASE}/node?operate=update_cfg&id={node_id}", json=cfg) as resp:
        resp.raise_for_status()
        print(f"resp.text:\n{resp.text}")
    print(f"successfully update config for {node_id}")

