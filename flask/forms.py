from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class HeadLoginForm(FlaskForm):
    hemail = StringField('Email',
                        validators=[DataRequired(), Email()])
    hpassword = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    pwd = PasswordField('New Password', validators=[DataRequired()])
    confirmpwd = PasswordField('Re-enter New Password',
                                     validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('Confirm')


class RegisterForm(FlaskForm):
    aname = StringField('Admin Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    amail = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    pwd = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('Sign Up')

class RemoveForm(FlaskForm):
    aid = IntegerField('Admin ID',
                        validators=[DataRequired()])
    submit = SubmitField('Remove')