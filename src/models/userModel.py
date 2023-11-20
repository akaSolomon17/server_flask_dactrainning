from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime,timedelta
from initSQL import db

class User(db.Model):
  user_id = db.Column(db.BIGINT, primary_key=True)
  first_name = db.Column(db.VARCHAR(255),unique = False, nullable = False)
  last_name = db.Column(db.VARCHAR(255),unique = False,nullable = False)
  email = db.Column(db.NVARCHAR(120),nullable = False)
  email_verified_at = db.Column(db.TIMESTAMP, default=datetime.now())
  password = db.Column(db.NVARCHAR(255),nullable = False)
  remember_token = db.Column(db.NVARCHAR(255))
  create_at = db.Column(db.TIMESTAMP, default=datetime.now())
  update_at = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now())
  image = db.Column(db.NVARCHAR(255), default="https://res.cloudinary.com/dooge27kv/image/upload/v1667982724/project/avatar.png")
  role_id = db.Column(db.Enum('1','2','3'),db.ForeignKey('roles.role_id'), nullable=False)

  role = db.relationship('Roles', backref=db.backref('users'), lazy=True)
    
  def __init__(self, first_name, last_name,email,password,role_id):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.role_id = role_id