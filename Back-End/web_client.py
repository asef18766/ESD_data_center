from flask import (
    Blueprint,
    request,
    make_response
)
from database.node.config import (
    get_node_config,
    update_node_config
)
from database.node.node import (
    get_node_instance,
    create_node
)
from database.node.user import (
    list_user_node,
    assign_node_owner,
    user_has_node,
    check_node_owner
)
from database.node.device import (
    dev_name_2_hid
)
from auth import login_required
import logging
import os

admin_token = os.getenv("ADMIN_TOKEN", "SUPER_ADMIN_TOKEN")
web_client_api = Blueprint("web_client_api", __name__)

@web_client_api.route("/create_node", methods=["POST"])
def create():
    data:dict = request.json
    if "admin_token" not in data:
        return make_response("token not found", 400)
    if data["admin_token"] != admin_token:
        return make_response("token_err", 403)
    
    logging.warning(f"create farm node {create_node('bogay1450')}")
    return "OK"

@web_client_api.route("/node", methods=["GET","POST"])
@login_required
def node(*args, **kwargs):
    action = request.args.get("operate")
    user_id = kwargs["user_id"]
    if action == "list_all":
        return make_response({"nodes":list_user_node(user_id)}, 200)

    elif action == "create":
        node_token:dict=request.json
        if "node_token" not in node_token:
            return make_response("format error", 403)
        node_token:str = node_token["node_token"]
        try:
            assign_node_owner(node_token, user_id)
            return make_response({"result":"success"},200)
        except IndexError:
            return make_response({"result":"not exsist"},200)
        except ValueError:
            return make_response({"result":"already taken"},200)
    
    elif action == "view_cfg":
        node_token:str = request.args.get("id")
        if not user_has_node(user_id, node_token):
            return make_response({"msg":"deny"}, 403)
        return make_response(get_node_config(node_token),200)
    
    elif action == "update_cfg":
        node_token:str = request.args.get("id")
        if not user_has_node(user_id, node_token):
            return make_response({"msg":"deny"}, 403)
        update_node_config(node_token, request.json)
        return "OK"
    
    elif action == "set_stat_cfg":
        '''
        this will check user's query and setup further query condition cache
        '''
        data:dict = request.json
        node_ids = check_node_owner(user_id, data["node_ids"])
        hids = dev_name_2_hid(node_ids, data["dev_name"])
        rule = data["group"]
        # WIP


    return make_response({"msg":"no such action"},404)
