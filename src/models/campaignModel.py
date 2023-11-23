import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from initSQL import db

class Campaign(db.Model):
    campaign_id = db.Column(NVARCHAR(16), primary_key=True, default=uuid.uuid4().bytes)
    name = db.Column(db.NVARCHAR(120), nullable=False)
    user_status = db.Column(Enum('ACTIVE', 'INACTIVE'), default='ACTIVE', nullable=False)
    budget = db.Column(db.INT, nullable=False)
    used_amount = db.Column(db.INT, nullable=False)
    usage_rate = db.Column(db.FLOAT, nullable=False)
    bid_amount = db.Column(db.INT, nullable=False)
    start_date = db.Column(db.DATETIME, nullable=False)
    end_date = db.Column(db.DATETIME, nullable=False)
    creative_id = db.Column(db.INT, nullable=False)
    user_id = db.Column(db.NVARCHAR(16), db.ForeignKey('user.user_id'),nullable=False)
    create_at = db.Column(db.TIMESTAMP, default=datetime.now())
    update_at = db.Column(db.TIMESTAMP, default=datetime.now())
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
        self.delete_flag = delete_flag