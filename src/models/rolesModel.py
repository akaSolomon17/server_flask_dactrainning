from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from initSQL import db

class Roles(db.Model):
    role_id = db.Column(db.Enum('1','2','3'),default='1', primary_key=True)
    role_name = db.Column(db.Enum('Admin', 'DAC', 'Advertiser'), default = 'Admin', nullable=False,unique=True)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

