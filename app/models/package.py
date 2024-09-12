from app import db
from datetime import datetime

class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(36), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(30), nullable=False)
    sender_address = db.Column(db.Text, nullable=False)
    recipient_address = db.Column(db.Text, nullable=False)
    delivery_deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)