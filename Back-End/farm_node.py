from flask import (
    Blueprint,
    request,
    make_response
)
from .database.node_control import (
    get_node_instance
)

farm_node_api = Blueprint("farm_node_api", __name__)

@farm_node_api.route("/ping", methods=["GET"])
def ping():
    return make_response({"msg":"i am alive"},200)

@farm_node_api.route("/register", methods=["POST"])
def register():
    data:dict = request.json
    node = get_node_instance(data["token"])