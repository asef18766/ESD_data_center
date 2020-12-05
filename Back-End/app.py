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

app.register_blueprint(auth_api)
app.register_blueprint(farm_node_api, url_prefix = "/endpoint")
app.register_blueprint(web_client_api)

if __name__ == "__main__":
    app.run()