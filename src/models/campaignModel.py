from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from initSQL import db

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
        self.title = title
        self.description = description
        self.preview_image = preview_image
        self.final_url = final_url
        self.user_update = user_update
        self.delete_flag = delete_flag