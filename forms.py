from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PatientForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    age = IntegerField('Age')
    email = StringField('Email')
    phone = StringField('Phone')
    submit = SubmitField('Add Patient')

class AppointmentForm(FlaskForm):
    hospital = SelectField('Hospital', coerce=int, validators=[DataRequired()])
    doctor = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    patient = SelectField('Patient', coerce=int, validators=[DataRequired()])
    when = DateTimeField('Date & Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')
