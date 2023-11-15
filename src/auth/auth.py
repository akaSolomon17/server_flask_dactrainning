import jwt, os


from flask import Flask, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class pyjwtAuthMiddleware(Resource):
    try:
        pass
    except:
        pass