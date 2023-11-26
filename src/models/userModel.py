import uuid,enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Enum

from datetime import datetime,timedelta
from initSQL import db
# from .rolesModel import RoleId
  
class User(db.Model):
  user_id = db.Column(db.NVARCHAR(16), primary_key=True, default=uuid.uuid4())
  email = db.Column(db.NVARCHAR(120), nullable = False)
  password = db.Column(db.NVARCHAR(150), nullable = False)
  first_name = db.Column(db.VARCHAR(150), nullable = False)
  last_name = db.Column(db.VARCHAR(120), nullable = False)
  role_id = db.Column(db.Enum('ADMIN','DAC','ADVERTISER'), db.ForeignKey('roles.role_id'), nullable=False,default='ADMIN')
  address = db.Column(db.VARCHAR(255), nullable = False)
  phone = db.Column(db.VARCHAR(11), nullable = False, unique = True)
  avatar = db.Column(db.NVARCHAR(255), default="https://res.cloudinary.com/dooge27kv/image/upload/v1667982724/project/avatar.png")
  actions = db.Column(db.VARCHAR(150), nullable = True)
  create_at = db.Column(db.TIMESTAMP, default=datetime.now())
  update_at = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now())
  delete_flag = db.Column(db.BOOLEAN, default=False)
  
  role = db.relationship('Roles', backref=db.backref('users'), lazy=True)
    
  def __init__(self, first_name, last_name,email,password,role_id,delete_flag):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.phone = phone
    self.avatar = avatar
    self.actions = actions
    self.delete_flag = delete_flag
    self.address = address
    self.role_id = role_id
    self.delete_flag = delete_flag