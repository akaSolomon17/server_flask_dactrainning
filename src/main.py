import os, json, sys

from flask import Flask
from flask_restful import Api, Resource

from dotenv import load_dotenv
from routes.userRoute import initialRoutes
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# app.secret_key = "SecretKey"


# Load variables in .env environment
load_dotenv()
DB_URL = os.getenv('DB_URL')

# Initialize DB SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    createTable = db.create_all()
    if createTable is not None:
        print("\n Error create models!")
    else:
        print("\n Models are all created successfully!")
        
# Routes
initialRoutes(api)

if __name__ == "__main__":
    app.run(debug=True)
