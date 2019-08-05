from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.tablegateways import UserTableGateway


class SearchForm(FlaskForm):
    search_input = TextField('Find', validators=[DataRequired()])
    submit = SubmitField('Find')


class LoginForm(FlaskForm):
    login = TextField('Login', validators=[DataRequired(), Length(
        max=60, message="Login must be smoller than 60 lenght")])
    password = TextField('Password', validators=[DataRequired(), Length(
        max=60, message="Password must be smoller than 60 lenght")])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    login = TextField('Login', validators=[DataRequired(), Length(max=60)])
    password = TextField('Password', validators=[
                         DataRequired(), Length(max=60)])
    password_repeat = TextField("Repeat password", validators=[
                                DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Register')

    def validate_login(self, login):
        login_is_exists = UserTableGateway.login_is_exists(login.data)
        if login_is_exists:
            raise ValidationError("Please use a different username.")


class EditProfileForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(max=60)])
    about_me = TextAreaField('About me', validators=[Length(max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_login, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_login = original_login

    def validate_login(self, login):
        if login.data != self.original_login:
            is_login_extsts = UserTableGateway.login_is_exists(login.data)
            if is_login_extsts:
                raise ValidationError('Please use a different username.')
