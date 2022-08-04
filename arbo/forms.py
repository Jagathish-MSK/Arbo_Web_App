from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp

class Registration(Form):
    user_name = StringField(label='Username', validators=[DataRequired(), Length(min=5, max=20), Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    email = StringField(label='Email Id' ,validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=15),  Regexp("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", message="Minimum eight characters, at least one letter, one number and one special character:")])
    retype = PasswordField(label='Re Enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='SignUp')

class Login(Form):
    user_name = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=15)])
    login = SubmitField(label='Login')