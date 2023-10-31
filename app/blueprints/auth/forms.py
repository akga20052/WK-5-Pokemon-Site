from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, EmailField, PasswordField, HiddenField
from wtforms.validators import DataRequired, EqualTo

class PokemaneForm(FlaskForm):
    pokemane = StringField('Enter Pokemon Name or Number:', validators=[DataRequired()])
    submit_btn = SubmitField(('Submit'))
    pokemanes_dict = HiddenField()


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField(('Register'))

class LoginForm(FlaskForm):
    email = EmailField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Sign In')