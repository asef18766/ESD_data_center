from flask import (
    Flask,
    request
)

from database.node_control import *
from auth import *
from datetime import timedelta
import logging
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

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

app.register_blueprint(api)

if __name__ == "__main__":
    app.run()