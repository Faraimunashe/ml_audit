from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import datetime, date, time, timedelta
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@company.com", "autofocus": True, "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField('Login Account')
   

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register Account')
        


class UploadCSVForm(FlaskForm):
    file = FileField('Transaction CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload & Audit')



class UserForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=100)
    ])
    
    name = StringField('Full Name', validators=[
        DataRequired(), Length(max=100)
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    
    role = SelectField('Role', choices=[
        ('1', 'Admin'),
        ('2', 'Auditor')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Save User')