import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from initSQL import db
import enum

class CampaignStatus(enum.Enum):
    ACTIVE = 'ACTIVE',
    INACTIVE = 'INACTIVE',
    
class Campaign(db.Model):
    campaign_id = db.Column(db.NVARCHAR(16), primary_key = True, default=uuid.uuid4().bytes)
    name = db.Column(db.NVARCHAR(120), nullable=False)
    user_status = db.Column(db.Enum(CampaignStatus), default = CampaignStatus.ACTIVE, nullable=False)
    budget = db.Column(db.INT, nullable=False)
    bid_amount = db.Column(db.INT, nullable=False)
    creative_id = db.Column(db.NVARCHAR(16), db.ForeignKey('creative.creative_id'), nullable=False,default=uuid.uuid4().bytes)
    user_id = db.Column(db.NVARCHAR(16), db.ForeignKey('user.user_id'),nullable=False)
    used_amount = db.Column(db.INT, nullable=False)
    usage_rate = db.Column(db.FLOAT, nullable=False)
    start_date = db.Column(db.DATETIME, nullable=False)
    end_date = db.Column(db.DATETIME, nullable=False)
    create_at = db.Column(db.TIMESTAMP, default=datetime.now())
    update_at = db.Column(db.TIMESTAMP, default=datetime.now())
    delete_flag = db.Column(db.BOOLEAN, default=False)
    
    user = db.relationship('User',backref = db.backref('campaign'), lazy=True)
    creative = db.relationship('Creative',backref = db.backref('campaign'), lazy=True)
    def __init__(self,name,status, used_amount,usage_rate,budget,bid_amount,start_date,end_date,title,description,preview_image,final_url,user_update,delete_flag,creative_id,user_id):
        self.name = name
        self.status = status
        self.used_amount = used_amount
        self.usage_rate = usage_rate
        self.budget = budget
        self.bid_amount = bid_amount
        self.start_date = start_date
        self.end_date = end_date
        self.delete_flag = delete_flag
        self.creative_id = creative_id
        self.user_id = user_id
        