from . import *

from flask import request
from logging import (
    error,
    info
)
import requests

def send_msg(node_id:str, msg:str):
    info(f"sending line message to url:{LINE_BOT_API_BASE}/farm_notify")
    with requests.post(f"{LINE_BOT_API_BASE}/farm_notify", json={"msg":msg, "farm_token":node_id, "DATA_CENTER_TOKEN":DATA_CENTER_TOKEN}) as resp:
        if resp.status_code != 200:
            error(resp.text)
            raise Exception(f"got status code {resp.status_code}, with content {resp.text}")    

def line_bot_token_required(func):
    '''
    this function will check for argument LINE_BOT_CLIENT_TOKEN in request body
    '''
    def wrapper(*args, **kwargs):
        info(f"raw check node data :{request.data}")
        data = request.json
        if data["LINE_BOT_CLIENT_TOKEN"] == LINE_BOT_CLIENT_TOKEN:
            return func(*args, **kwargs)
        else:
            raise ValueError("client auth failure")

    return wrapper