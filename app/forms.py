from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = DecimalField('Price', validators=[DataRequired()])
    material = StringField('Material')
    weight = StringField('Weight')
    carat = StringField('Carat')
    color = StringField('Color')
    clarity = StringField('Clarity')
    country_of_origin = StringField('Country of Origin')
    image = FileField('Product Image')
    submit = SubmitField('Upload Product')

class MerchantForm(FlaskForm):
    merchant_name = StringField('Merchant Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    contact_info = StringField('Contact Information')
    submit = SubmitField('Save Profile')