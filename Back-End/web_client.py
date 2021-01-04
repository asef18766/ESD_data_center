from flask import (
    Blueprint,
    request,
    make_response,
    send_file
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
from database.node.devlog import (
    get_all_dev_log
)
from cache.query import (
    set_user_query_prefer,
    get_user_prefer,
    execute_query
)
from cache.node_config import (
    load_lastest_node_cfg
)
from utils import (
    str_to_datetime,
    export_devlog_to_file
)
from auth import login_required
import json
import logging
import os
from logging import (
    error
)
from traceback import format_exc
from uuid import uuid4
from celery_app.client import test_connect

admin_token = os.getenv("ADMIN_TOKEN", "SUPER_ADMIN_TOKEN")
web_client_api = Blueprint("web_client_api", __name__)
DEFAULT_MAX_RECORD = 48763

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
        try:
            user_config = request.json
            node:FarmNode = get_node_instance(node_token)
            if node is None:
                raise IndexError(f"can not found node {node_token}")

            # check for connection
            #if not test_connect(node_token, user_config["configures"]):
            #    raise ConnectionError(f"can not link to target device with config {user_config['configures']}")

            update_node_config(node_token, user_config)
            #load_lastest_node_cfg(node_token)
            
        except Exception as e:
            error(format_exc())
            return make_response({"msg":"invaild config"}, 400)
        return "OK"
    
    elif action == "set_stat_cfg":
        '''
        this will check user's query and setup further query condition cache
        '''
        data:dict = request.json
        
        node_ids = check_node_owner(user_id, data["node_ids"])
        try:
            hids, pics = dev_name_2_hid(node_ids, data["dev_name"])
        except IndexError as e:
            if str(e).startswith("device name"):
                return make_response({"msg":"invaild device name"}, 404)
            raise e

        rule = data["group"]
        user_cfg = {}
        
        target_hids = []
        for dn, hidl in hids.items():
            user_cfg.update({
                dn:{
                    "target_hids":hidl,
                    "icon_link":pics[dn]
                }
            })
            target_hids += hidl
        set_user_query_prefer(user_id, target_hids, rule, user_cfg)
        return make_response("OK", 200)
    
    elif action == "v_stat":
        return make_response(execute_query(user_id), 200) 
    
    elif action == "get_s_pref":
        return make_response(get_user_prefer(user_id), 200)
    
    elif action == "download_ss":
        data:dict = request.json
        ts_start = str_to_datetime(data["ts_range"]["gt"])
        ts_end = str_to_datetime(data["ts_range"]["lt"])
        limit = DEFAULT_MAX_RECORD
        if "max_record_count" in data:
            limit = data["max_record_count"]
        # TODO: testing
        logs = get_all_dev_log(data["node_id"], data["hids"], ts_start, ts_end, limit)
        fname = f"/tmp/{str(uuid4())}.xlsx"
        export_devlog_to_file(logs, fname)
        return send_file(fname, attachment_filename="res.xlsx")

    return make_response({"msg":"no such action"},404)