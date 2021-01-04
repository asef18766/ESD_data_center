from requests import Session
from config import API_BASE
import json
import click
from auth import default_auth

@default_auth
def download_xml(sess:Session, file:str):
    if file == "":
        print("please insert constraint file")
        return
    
    payload = json.loads(open(file, "r").read())
    print("send request")
    with sess.get(f"{API_BASE}/node?operate=download_ss", json=payload) as resp:
        print("receiving response")
        resp.raise_for_status()
        with open("result.xlsx", 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)