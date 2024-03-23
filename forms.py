""" consider all fields for accuracy
    consider all validations and error handling"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, TextAreaField, BooleanField, SelectField

class AddInspectionForm(FlaskForm):

    team_id = SelectField("Installation Team")
    sitter_id = IntegerField("Inspection Sitter ID")
    job_number = IntegerField("Job Number from Job Nimbus")
    date = DateField("Inspection Date")
    type = SelectField("Type of Inspection",
                       choices=[('battery', 'Battery'),
                                ('building framing', 'Building Framing'),
                                ('building in-progress', 'Building In-progress'),
                                ('change of service', 'Change of Service'),
                                ('columns', 'Columns'),
                                ('electrical grounding', 'Electrical Grounding'),
                                ('final building', 'Final Building'),
                                ('final electrical', 'Final Electrical'),
                                ('final fire', 'Final Fire'),
                                ('final meter release', 'Final Meter Release'),
                                ('final roofing', 'Final Roofing'),
                                ('final solar', 'Final Solar'),
                                ('disconnect/reconnect', 'Disconnect/Reconnect'),
                                ('final zoning', 'Final Zoning'),
                                ('footer', 'Footer'),
                                ('foundation', 'Foundation'),
                                ('historical', 'Historical'),
                                ('mounting-rail bond', 'Mounting-rail Bond'),
                                ('pe certification', 'PE Certification'),
                                ('pre-power', 'Pre-power'),
                                ('pre-release', 'Pre-release'),
                                ('rough electrical', 'Rough Electrical'),
                                ('rough fire', 'Rough Fire'),
                                ('rough solar', 'Rough Solar'),
                                ('solar pv in-progress', 'Solar PV In-progress'),
                                ('solar rack tie-down', 'Solar Rack Tie-down'),
                                ('solar concealed attachments', 'Solar Concealed Attachments'),
                                ('special inspector form', 'Special Inspector Form'),
                                ('structural misc', 'Structural Misc'),
                                ('time of installation', 'Time of Installation'),
                                ('torque release', 'Torque Release'),
                                ('work with', 'Work With')])
    result = SelectField("Inspection Result", 
                         choices=[('pending', 'Pending'),
                                ('cancel', 'Cancel'),
                                ('fail', 'Fail'),
                                ('partial', 'Partial'),
                                ('pass', 'Pass'),
                                ('rescheduled', 'Rescheduled')])
    notes = TextAreaField("Inspection Notes")
    to_close = BooleanField("Will this inspection close the project?")
    at_fault = BooleanField("Is the team at fault for failing?")

