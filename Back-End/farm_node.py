from flask import (
    Blueprint,
    request,
    make_response
)
from database.node.device import (
    register_devices,
)
from cache.dev_map import (
    create_map
)
from cache.record import (
    write_cache
)
import logging
import uuid

farm_node_api = Blueprint("farm_node_api", __name__)

@farm_node_api.route("/ping", methods=["GET"])
def ping():
    return make_response({"msg":"i am alive"},200)

@farm_node_api.route("/register", methods=["POST"])
def register():
    try:
        data:dict = request.json
        i_serial, o_serial = register_devices(data["token"], data["input_devices"], data["output_devices"])
        return make_response({
            "success":True,
            "device_map":create_map(data["token"], i_serial + o_serial)
        })
    except Exception as e:
        logging.error(e)
        return make_response({"success":False}, 400)

@farm_node_api.route("/send_data", methods=["POST"])
def receiver():
    data:dict = request.json
    try:
        write_cache(data)
    except IndexError as e:
        logging.error(e)
        return make_response("invaild", 400)

    return make_response("OK")
