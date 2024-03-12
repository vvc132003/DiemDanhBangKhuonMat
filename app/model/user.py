
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)

    # Tạo mối quan hệ với bảng AttendanceRecords
    attendance_records = db.relationship('AttendanceRecords', back_populates='user')

    def __repr__(self):
        return f"User(id={self.id}, hovaten={self.hovaten}, anhdaidien={self.anhdaidien})"


class AttendanceRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    checkInTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_in_out_type = db.Column(db.String(255), nullable=True)

    # Tạo mối quan hệ với bảng Users
    user = db.relationship('Users', back_populates='attendance_records')

    def __repr__(self):
        return f"AttendanceRecord(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})"

