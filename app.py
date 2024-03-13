from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Building_dept, Client, Installation_team, Project, Inspection, Bd_contact, Inspection_sitter
from sqlalchemy import text

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///inspection_tracker_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] =  "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    """Show home page"""
    return render_template('index.html')

@app.route('/inspection_scheduling')
def show_inspection_scheduling():
    """Show inspection scheduling options"""
    return render_template('inspection_scheduling.html')

@app.route('/dashboard')
def show_dashboard():
    """Show inspections dashboard"""
    return render_template('dashboard.html')