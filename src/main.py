import os, json, sys

from flask import Flask
from flask_restful import Api, Resource

from dotenv import load_dotenv
from routes.userRoute import initialRoutes
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,UTC
# from models.initDB import dbInit, db

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


# campaignModel
class Campaign(db.Model):
    campaign_id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.NVARCHAR(120), nullable=False)
    status = db.Column(db.Enum('ACTIVE', 'INACTIVE'), default='ACTIVE', nullable=False)
    used_amount = db.Column(db.BIGINT, nullable=False)
    usage_rate = db.Column(db.FLOAT, nullable=False)
    budget = db.Column(db.BIGINT, nullable=False)
    bid_amount = db.Column(db.BIGINT, nullable=False)
    start_date = db.Column(db.TIMESTAMP, nullable=False)
    end_date = db.Column(db.TIMESTAMP, nullable=False)
    title = db.Column(db.NVARCHAR(120), nullable=False)
    description = db.Column(db.NVARCHAR(255), nullable=False)
    preview_image = db.Column(db.VARCHAR(255), nullable=False)
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.user_id'),nullable=False)
    final_url = db.Column(db.NVARCHAR(255), nullable=False)
    user_update = db.Column(db.BIGINT, nullable=False)
    create_at = db.Column(db.TIMESTAMP, default=datetime.now(UTC))
    update_at = db.Column(db.TIMESTAMP, default=datetime.now(UTC))
    delete_flag = db.Column(db.BOOLEAN, default=False)
    
    user = db.relationship('User',backref = db.backref('campaign'), lazy=True)
    
    def __init__(self,name,status, used_amount,usage_rate,budget,bid_amount,start_date,end_date,title,description,preview_image,final_url,user_update,delete_flag):
        self.name = name
        self.status = status
        self.used_amount = used_amount
        self.usage_rate = usage_rate
        self.budget = budget
        self.bid_amount = bid_amount
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.description = description
        self.preview_image = preview_image
        self.final_url = final_url
        self.user_update = user_update
        self.delete_flag = delete_flag
# rolesModel
class User(db.Model):
    user_id = db.Column(db.BIGINT, primary_key=True)
    first_name = db.Column(db.VARCHAR(255),unique = False, nullable = False)
    last_name = db.Column(db.VARCHAR(255),unique = False,nullable = False)
    email = db.Column(db.NVARCHAR(120),nullable = False)
    email_verified_at = db.Column(db.TIMESTAMP, default=datetime.now(UTC))
    password = db.Column(db.NVARCHAR(255),nullable = False)
    remember_token = db.Column(db.NVARCHAR(255),nullable = False)
    create_at = db.Column(db.TIMESTAMP, default=datetime.now(UTC))
    update_at = db.Column(db.TIMESTAMP, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    image = db.Column(db.NVARCHAR(255), nullable=False)
    role_id = db.Column(db.Enum('1','2','3'),db.ForeignKey('roles.role_id'), nullable=False)

    role = db.relationship('Roles', backref=db.backref('users'), lazy=True)
    
    def __init__(self, first_name, last_name,email,password,remember_token,image):
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.password = password
      self.remember_token = remember_token
      self.image = image
# userModel
class Roles(db.Model):
    role_id = db.Column(db.Enum('1','2','3'), primary_key=True)
    role_name = db.Column(db.Enum('Admin', 'DAC', 'Advertiser'), default = 'Admin', nullable=False,unique=True)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

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
