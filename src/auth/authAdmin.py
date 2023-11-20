import jwt, os,json

from flask import Flask, request, make_response

from configs.errorStatus import errorStatus

from functools import wraps

def authMiddlewareAdmin(func):
    @wraps(func)
    def middlewareAdmin(*args, **kwargs):
        from initSQL import db
        from models.userModel import User
        try:
            json = request.get_json()
            user_id = json['user_id']
            
            User = User.query.filter_by(user_id = user_id).one_or_404("Not found account!")
        
            if User.role_id != "1":
                return errorStatus.statusCode("Admin resources access denied.",500)
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
            
    return middlewareAdmin