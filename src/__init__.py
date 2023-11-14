import os, json, sys

from flask import Flask
from flask_restful import Api, Resource

from routes.userRoute import initialRoutes


app = Flask(__name__)
api = Api(app)

initialRoutes(api)

if __name__ == "__main__":
    app.run(debug=True)
