import enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from initSQL import db


class RoleId(enum.Enum):
  ADMIN = '1',
  MANAGER = '2',
  USER = '3'
  
  
class RoleName(enum.Enum):
  ADMIN = 'Admin',
  MANAGER = 'DAC',
  USER = 'Advertiser'

class Roles(db.Model):
    role_id = db.Column(db.Enum(RoleId),default= RoleId.ADMIN, primary_key=True)
    role_name = db.Column(db.Enum(RoleName), default = RoleName.ADMIN, nullable=False,unique=True)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

