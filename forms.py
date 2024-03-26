""" consider all fields for accuracy
    consider all validations and error handling"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional

# Building department forms

class AddBuildingDepartment(FlaskForm):
    """Form for adding/editing a building department"""

    state = StringField("State")
    county = StringField("County")
    city = StringField("City")
    name = StringField("Building Department Name")
    rough_required = BooleanField("Is a rough inspection required?")
    pe_cert_required = BooleanField("Is a PE Certification required?")
    type_of_pe_cert = StringField("Type of PE Certification required")
    pe_cert_notes = TextAreaField("PE Certification Notes")
    shutdown_procedure = TextAreaField("Shutdown procedure for the jurisdiction")
    website = StringField("Link to building department's website")
    inspection_portal = StringField("Link to the building department's inspection portal")
    contact_list = StringField("Link to the building department's contact list")
    notes = TextAreaField("General notes about this building department")

# Client forms

class AddClient(FlaskForm):
    """Form for adding/editing a client"""

    first_name = StringField("Client First Name")
    last_name = StringField("Client Last Name")
    notes = StringField("Client Notes")

# Project Forms

class AddProject(FlaskForm):
    """Form for adding a project to a specific client"""

    client_id = SelectField("Please select a client")   
    bd_id = SelectField("Please select a building deptartment below")
    job_number = IntegerField("Enter the Job Nimbus job number") 
    job_link = StringField("Link to project in Job Nimbus")
    description = StringField("Description of the project")
    kws = FloatField("How many kWs is the project?")

# Inspection forms

class AddInspectionForm(FlaskForm):
    """Form for adding/editing and inspection"""

    team_id = SelectField("Installation Team")
    sitter_id = IntegerField("Inspection Sitter ID", validators=[Optional()])
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
