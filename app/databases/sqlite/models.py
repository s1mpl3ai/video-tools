import datetime 
from app.databases.sqlite.connection import Database
from tzlocal import get_localzone

db = Database().db

class Video(db.Model): 
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255),unique = True, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(50), nullable=True)
    length = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.now(get_localzone()))
    


