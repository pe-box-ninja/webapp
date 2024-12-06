from app import db
from datetime import datetime
from enum import Enum


class AssignmentStatus(Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    @staticmethod
    def list():
        return [status.value for status in AssignmentStatus]


class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey("courier.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"))
    parcel_locker_id = db.Column(db.Integer, db.ForeignKey("parcel_locker.id"))
    status = db.Column(db.String(64), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime)

    package = db.relationship("Package", backref="assignments")
    courier = db.relationship("Courier", backref="assignments")
    warehouse = db.relationship("Warehouse", backref="assignments")
    parcel_locker = db.relationship("ParcelLocker", backref="assignments")
