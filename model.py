from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Admin', 'Manager', 'Tenant', name='user_roles'), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    rent = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('Available', 'Occupied', name='room_status'), default='Available')


class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    move_in_date = db.Column(db.Date)
    move_out_date = db.Column(db.Date)
    user = db.relationship('User', backref='tenants', lazy=True)
    room = db.relationship('Room', backref='tenants', lazy=True)


class ProblemReport(db.Model):
    __tablename__ = 'problem_reports'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('Pending', 'Resolved', name='report_status'), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant = db.relationship('Tenant', backref='problem_reports', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Paid', 'Unpaid', name='payment_status'), default='Unpaid')
    tenant = db.relationship('Tenant', backref='payments', lazy=True)


class ManagementAction(db.Model):
    __tablename__ = 'management_actions'
    id = db.Column(db.Integer, primary_key=True)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(100))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='management_actions', lazy=True)
