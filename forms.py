""" consider all fields for accuracy
    consider all validations and error handling"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, TextAreaField, BooleanField, SelectField

class AddInspectionForm(FlaskForm):

    team_id = IntegerField("Installation Team ID")
    sitter_id = IntegerField("Inspection Sitter ID")
    project_id = IntegerField("Project ID")
    date = DateField("Inspection Date")
    type = StringField("Type of Inspection")
    result = StringField("Inspection Result")
    notes = TextAreaField("Inspection Notes")
    to_close = BooleanField("Will this inspection close the project?")
    at_fault = BooleanField("Is the team at fault for failing?")

