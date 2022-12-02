from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField

class PatientAppForm(FlaskForm): 
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    date_of_birth = StringField('Date of Birth')
    submit = SubmitField('Search')