"""review queries to be sure using new convention db.session.execute(db.select())"""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Building_dept, Client, Installation_team, Project, Inspection, Bd_contact, Inspection_sitter
from sqlalchemy import text
from datetime import datetime, date, timedelta

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

#Views related to scheduling

@app.route('/inspection_scheduling')
def show_inspection_scheduling():
    """Show inspection scheduling options"""

    return render_template('inspection_scheduling.html')

@app.route('/yesterdays_schedule')
def show_yesterdays_schedule():
    """Shows yesterday schedule"""

    schedule_date = date.today() - timedelta(days=1)
    inspections = Inspection.query.filter(Inspection.date==schedule_date).all()
    return render_template('schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/todays_schedule')
def show_todays_schedule():
    """Shows today schedule"""

    schedule_date = date.today()
    inspections = Inspection.query.filter(Inspection.date==schedule_date).all()
    return render_template('schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/tomorrows_schedule')
def show_tomorrows_schedule():
    """Shows tomorrows schedule"""

    schedule_date = date.today() + timedelta(days=1)
    inspections = Inspection.query.filter(Inspection.date==schedule_date).all()
    return render_template('schedule.html', schedule_date=schedule_date, inspections=inspections)

# Views related to dashboard and reporting

@app.route('/dashboard')
def show_dashboard():
    """Show inspections dashboard"""

    return render_template('dashboard.html')

# Views related to updating db information i.e. adding/editing clients, building departments, contacts etc

@app.route('/update_db')
def show_update_db_menu():
    """Shows landing page for updating database"""

    return render_template('update_db.html')

@app.route('/building_depts')
def show_building_depts():
    """Show building depts landing page"""

    building_depts = db.session.execute(db.select(Building_dept).order_by(Building_dept.name)).scalars()
    return render_template('building_depts.html', building_depts=building_depts)

@app.route('/building_depts/<int:bdid>')
def show_bd_details(bdid):
    """Show details on a specific building dept"""

    bd = Building_dept.query.get_or_404(bdid)
    return render_template('bd_details.html', bd=bd)

@app.route('/building_depts/<int:bdid>/edit')
def show_edit_bd_form(bdid):
    """Show form to edit a specific building department"""

    bd = Building_dept.query.get_or_404(bdid)
    return render_template("edit_bd.html", bd=bd)

@app.route('/clients/<int:cid>')
def show_client_details(cid):
    """Show details on a specific client"""

    client = Client.query.get_or_404(cid)
    return render_template('client_details.html', client=client)
