from flask import (
    Flask,
    request,
    make_response
)

from auth import *
from farm_node import *
from web_client import *
from line import line_api
from datetime import timedelta
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename='runtime.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = Flask(__name__)

app.register_blueprint(auth_api)
app.register_blueprint(farm_node_api, url_prefix = "/endpoint")
app.register_blueprint(web_client_api)
app.register_blueprint(line_api, url_prefix = "/line")

if __name__ == "__main__":
    app.run()