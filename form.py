from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class Login(FlaskForm):
    adminname = StringField('Admin Id :',validators=[DataRequired(),Length(min=2,max=6)])
    password = PasswordField('Password :',validators=[DataRequired()])
    submit = SubmitField('Login')