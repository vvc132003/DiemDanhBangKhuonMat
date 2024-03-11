# /app/models/attendance.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AttendanceRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"AttendanceRecord(id={self.id}, user_name={self.user_name}, timestamp={self.timestamp})"


# /app/models/user.py

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hovaten = db.Column(db.String(255), nullable=True)
    anhdaidien = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, hovaten={self.hovaten}, anhdaidien={self.anhdaidien})"
