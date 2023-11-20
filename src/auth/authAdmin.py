import jwt, os,json

from flask import Flask, request, make_response
from dotenv import load_dotenv
from configs.errorStatus import errorStatus

from functools import wraps

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def authMiddlewareAdmin(func):
    @wraps(func)
    def middlewareAdmin(*args, **kwargs):
        from initSQL import db
        from models.userModel import User
        try:
            token = request.headers.get("Authorization")
            if not token:
                return errorStatus.statusCode("Invalid Authentication.", 400)

            user = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])

            if user['payload'] != 1:
                return errorStatus.statusCode("Admin resources access denied.",500)
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
            
    return middlewareAdmin