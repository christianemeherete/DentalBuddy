from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ReceptionForm(FlaskForm):
    firstname = StringField('First name')

    middlename = StringField('Middle name')

    lastname = StringField('Last name')

    role = StringField('Role')

    gender = StringField('Gender')

    email = StringField('Email')

    SSN = StringField('SSN')

    streetname = StringField('Street name')

    streetnum = StringField('Street number')

    apartnum = StringField('Apartment number')

    city = StringField('City')

    province = StringField('Province')

    postalcode = StringField('Postal code')

    date = StringField('Date of Birth')

    submit = SubmitField('Submit')
