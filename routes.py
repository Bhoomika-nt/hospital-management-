from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import User, Hospital, Doctor, Patient, Appointment
from .forms import SignupForm, LoginForm, PatientForm, AppointmentForm
from datetime import datetime

bp = Blueprint('bp', __name__)

# Home with background, shows 3 featured hospitals
@bp.route('/')
def home():
    featured = Hospital.query.limit(3).all()
    return render_template('home.html', hospitals=featured)

# Signup / login
@bp.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter((User.email==form.email.data)|(User.username==form.username.data)).first():
            flash('User exists','warning')
        else:
            u = User(username=form.username.data, email=form.email.data)
            u.set_password(form.password.data)
            db.session.add(u); db.session.commit()
            flash('Created — please sign in','success')
            return redirect(url_for('bp.login'))
    return render_template('signup.html', form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            session['user'] = u.username
            session['user_id'] = u.id
            flash('Signed in','success')
            return redirect(url_for('bp.home'))
        flash('Invalid credentials','danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bp.home'))

# Hospitals list (all)
@bp.route('/hospitals')
def hospitals():
    allh = Hospital.query.all()
    return render_template('hospitals.html', hospitals=allh)

# Doctors of a hospital
@bp.route('/hospitals/<int:hid>/doctors')
def doctors(hid):
    h = Hospital.query.get_or_404(hid)
    docs = Doctor.query.filter_by(hospital_id=hid).all()
    return render_template('doctors.html', hospital=h, doctors=docs)

# Add patient (to a chosen hospital)
@bp.route('/hospitals/<int:hid>/patients/add', methods=['GET','POST'])
def add_patient(hid):
    h = Hospital.query.get_or_404(hid)
    form = PatientForm()
    if form.validate_on_submit():
        p = Patient(name=form.name.data, age=form.age.data, email=form.email.data, phone=form.phone.data, hospital_id=hid)
        db.session.add(p); db.session.commit()
        flash('Patient added','success')
        return redirect(url_for('bp.doctors', hid=hid))
    return render_template('patients.html', hospital=h, form=form)

# Doctor schedule view
@bp.route('/hospitals/<int:hid>/schedules')
def schedule(hid):
    h = Hospital.query.get_or_404(hid)
    docs = Doctor.query.filter_by(hospital_id=hid).all()
    return render_template('schedule.html', hospital=h, doctors=docs)

# Appointments: book & list
@bp.route('/appointments', methods=['GET','POST'])
def appointments():
    form = AppointmentForm()
    form.hospital.choices = [(h.id,h.name) for h in Hospital.query.order_by(Hospital.name).all()]
    # default doctor/patient choices empty until hospital selected on client side; for simplicity fill all:
    form.doctor.choices = [(d.id,d.name) for d in Doctor.query.order_by(Doctor.name).all()]
    form.patient.choices = [(p.id,p.name) for p in Patient.query.order_by(Patient.name).all()]

    if form.validate_on_submit():
        ap = Appointment(hospital_id=form.hospital.data, doctor_id=form.doctor.data, patient_id=form.patient.data, when=form.when.data)
        # update rooms: check availability
        h = Hospital.query.get(form.hospital.data)
        if h.rooms_booked >= h.rooms_total:
            flash('No rooms available in selected hospital','danger')
            return redirect(url_for('bp.appointments'))
        h.rooms_booked += 1
        db.session.add(ap); db.session.commit()
        flash('Appointment booked','success')
        return redirect(url_for('bp.appointments'))

    appts = Appointment.query.order_by(Appointment.when.desc()).all()
    return render_template('appointments.html', form=form, appointments=appts)
