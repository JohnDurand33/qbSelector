from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class SignUpForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField('Sign In')

