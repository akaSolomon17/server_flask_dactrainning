import enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Enum

from initSQL import db

# class RoleId(enum.Enum):
#   ADMIN = '1',
#   DAC = '2',
#   ADVERTISER = '3'

class Roles(db.Model):
    role_id = db.Column(db.Enum('ADMIN','DAC','ADVERTISER'),default= 'ADMIN', primary_key=True)
    
    def __init__(self, role_id):
        self.role_id = role_id

