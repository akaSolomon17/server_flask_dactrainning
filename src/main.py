import os, json, sys

from flask import Flask
from flask_restful import Api, Resource

from dotenv import load_dotenv
from routes.userRoute import initialRoutes
from flask_sqlalchemy import SQLAlchemy

from models.initDB import db
app = Flask(__name__)
api = Api(app)
app.secret_key = "SecretKey"

initialRoutes(api)

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
