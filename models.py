from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), default='patient')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self,p): self.password_hash = generate_password_hash(p)
    def check_password(self,p): return check_password_hash(self.password_hash,p)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(400))
    phone = db.Column(db.String(50))
    rooms_total = db.Column(db.Integer, default=20)
    rooms_booked = db.Column(db.Integer, default=0)

    doctors = db.relationship('Doctor', backref='hospital', lazy=True)
    patients = db.relationship('Patient', backref='hospital', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(150))
    # simple schedule string for demo - could be normalized
    schedule = db.Column(db.String(500), default='Mon-Fri 9:00-17:00')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    when = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='booked')
