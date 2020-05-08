from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from application.models import User

class LoginForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired()])
     password = PasswordField('Password', validators=[DataRequired()])
     remember_me = BooleanField('Remember Me')
     submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddBookForm(FlaskForm):
    title = StringField("Book's title", validators=[DataRequired()])
    author = StringField("Book's author", validators=[DataRequired()])
    image = StringField("Image's url",
            validators=[FileAllowed(["png", "jpeg", "jpg"], "Images only!")])
    description = TextAreaField("Description", validators=[Length(max=1000)])
    submit = SubmitField("Save")

class ISBNAddForm(FlaskForm):
    isbn = StringField("Input your ISBN...")
    submit = SubmitField("Add via ISBN")
    manual = SubmitField("Add Manually")

class EditDeleteForm(FlaskForm):
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
