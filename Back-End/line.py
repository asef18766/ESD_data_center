from flask import (
    Blueprint,
    request
)
from line_notify import (
    DATA_CENTER_TOKEN
)
from line_notify.message import (
    line_bot_token_required
)
from database.node.node import get_node_instance
from logging import (
    warning,
    info
)

line_api = Blueprint("line_api", __name__)

@line_api.route("/check_farm", methods = ["POST"])
@line_bot_token_required
def check_node():
    data:dict = request.json
    try:
        node = get_node_instance(data["farm_token"])
        if node is None:
            return {"DATA_CENTER_TOKEN":DATA_CENTER_TOKEN, "exsist":False}
    except Exception as e:
        warning(f"check node failed for {e}")
        return {"DATA_CENTER_TOKEN":DATA_CENTER_TOKEN, "exsist":False}
    
    return {"DATA_CENTER_TOKEN":DATA_CENTER_TOKEN, "exsist":True}
    