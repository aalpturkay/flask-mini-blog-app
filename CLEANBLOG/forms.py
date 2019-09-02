from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    post_text = TextAreaField('Post Text', validators=[DataRequired()])
    submit = SubmitField('Add Post')

class ContactForm(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message',validators=[DataRequired()])
    submit = SubmitField('Contact')