from flask import (
    Flask,
    request,
    make_response
)

from auth import *
from farm_node import *
from web_client import *
from datetime import timedelta
import logging

app = Flask(__name__)

'''
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/create_node")
def oao():
    logging.warning(f"create farm node {create_node('bogay1450')}")
    return "OK"

@app.route("/link_user_node")
def uwu():
    user_identity = request.args.get('u')
    node_token = request.args.get('nt')
    assign_node_owner(node_token, user_identity)

    logging.warning(f"add node to user")
    return "uwu"
'''

app.register_blueprint(auth_api)
app.register_blueprint(farm_node_api, url_prefix = "/endpoint")
app.register_blueprint(web_client_api)

if __name__ == "__main__":
    app.run()