import jwt
import os
import datetime
from flask import (
    Blueprint,
    request,
    make_response
)
from database.auth import *

EXPIRE_DURATION = datetime.timedelta(days=365)
JWT_KEY = os.getenv("JWT_SECRET", "I THINK IT'S LONG ENOUGH TO RESIST BRUTE FORCE")
JWT_NAME = "GGJWT"
auth_api = Blueprint("auth_api", __name__)

def craftJWT(user_id:str)->bytes:
    dic = {
        'exp': datetime.datetime.now() + EXPIRE_DURATION,
        'iat': datetime.datetime.now(),
        'iss': 'w33d-esd',
        'data': {
            'user_id': user_id,
        },
    }
    return jwt.encode(dic, JWT_KEY, algorithm='HS256')

def decodeJWT(session:bytes)->dict:
    s = jwt.decode(session, JWT_KEY, issuer='w33d-esd', algorithms=['HS256'])
    return s['data']

def login_required(func):
    def wrapper(*args, **kwargs):
        try:
            sess:str = request.cookies.get(JWT_NAME)
            kwargs.update(decodeJWT(sess.encode()))
        except Exception as e:
            print(e)
            return make_response({"error":"login required"}, 403)
        
        return func(*args, **kwargs)
    return wrapper

@auth_api.route("/register", methods=["POST"])
def register():
    try:
        data:dict = request.get_json()
        create_user(**data)
    finally:
        return make_response({"result":"failed"}, 400)

@auth_api.route("/login", methods=["GET"])
def login():
    data:dict = request.json
    print(f"receive data:{data}")
    if not check_user_exist(**data):
        return make_response({"result":"failed"}, 400)
    
    resp = make_response({"result":"success"}, 200)
    resp.set_cookie(JWT_NAME, value=craftJWT(data["identity"]).decode())
    return resp


# test route
# must be removed in the future 
@auth_api.route("/get_cookie" , methods = ["GET"])
def cook():
    resp = make_response({"result":"success"}, 200)
    resp.set_cookie("GG", value="shorter_cookie")
    return resp

# test route
# must be removed in the future 
@auth_api.route("/test", methods=["GET"])
@login_required
def test(*args, **kwargs):
    return "OAO?"
