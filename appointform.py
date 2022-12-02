from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class AppointForm(FlaskForm):

    pid = StringField('SSN')
    
    eid = StringField('Employee ID')

    date = StringField('Date of Birth')

    starttime = StringField('Start time')

    endtime = StringField('End time')

    appointtype = StringField('Appointment Type')

    status = StringField('Status')

    room = StringField('Room #')

    submit = SubmitField('Submit')
