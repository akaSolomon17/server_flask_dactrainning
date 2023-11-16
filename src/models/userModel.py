from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .initDB import db

class User(db.Model):
    user_id = db.Column(db.BIGINT, primary_key=True)
    first_name = db.Column(db.VARCHAR(255),unique = False, nullable = False)
    last_name = db.Column(db.VARCHAR(255),unique = False,nullable = False)
    email = db.Column(db.NVARCHAR(120),nullable = False)
    email_verified_at = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    password = db.Column(db.NVARCHAR(255),nullable = False)
    remember_token = db.Column(db.NVARCHAR(255),nullable = False)
    create_at = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_at = db.Column(db.TIMESTAMP, default=datetime.utcnow(), onupdate=datetime.utcnow())
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