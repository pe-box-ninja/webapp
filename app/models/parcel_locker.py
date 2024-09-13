from app import db
from datetime import datetime

class ParcelLocker(db.Model):
    __tablename__ = 'parcel_locker'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    total_compartments = db.Column(db.Integer, nullable=False)
    available_compartments = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)