import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from initSQL import db

class Creative():
    create_id
    title = db.Column(db.NVARCHAR(120), nullable=False)
    description = db.Column(db.NVARCHAR(255), nullable=False)
    preview_image = db.Column(db.VARCHAR(255), nullable=False)
    final_url = db.Column(db.NVARCHAR(255), nullable=False)
    status = db.Column(db.BOOLEAN, default=True, nullable=False)
        
    def __init__(self,title,description,preview_image,final_url):
        self.title = title
        self.description = description
        self.preview_image = preview_image
        self.final_url = final_url