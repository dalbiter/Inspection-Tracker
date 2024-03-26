"""review queries to be sure using new convention db.session.execute(db.select())"""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Building_dept, Client, Installation_team, Project, Inspection, Bd_contact, Inspection_sitter
from sqlalchemy import text
from datetime import datetime, date, timedelta
from forms import AddInspectionForm, AddBuildingDepartment, AddClient, AddProject

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

@app.route('/inspections')
def show_inspection_scheduling():
    """Show inspection scheduling options"""

    return render_template('inspections.html')

@app.route('/inspections/add', methods=['GET', 'POST'])
def handle_inspection_form():
    """Handles form to add a new inspection instance"""

    form = AddInspectionForm()
    teams = [(t.id, t.team_name.title()) for t in Installation_team.query.all()]
    form.team_id.choices = teams

    if form.validate_on_submit():
        team_id = form.team_id.data
        sitter_id = form.sitter_id.data
        job_number = form.job_number.data
        date = form.date.data
        type = form.type.data
        result = form.result.data
        notes = form.notes.data
        to_close = form.to_close.data
        at_fault = form.at_fault.data

        team = Installation_team.query.get_or_404(team_id)
        new_inspection = Inspection(team_id=team_id, 
                                    sitter_id=sitter_id, 
                                    project_job_number=job_number, 
                                    date=date, type=type, 
                                    result=result, notes=notes, 
                                    to_close=to_close, 
                                    at_fault=at_fault)
        db.session.add(new_inspection)
        db.session.commit()

        flash(f'Created new inspection for team: {team.team_name.title()} on {date}')
        return redirect('/inspections')
    else:
        return render_template('add_inspection.html', form=form)
    
@app.route('/inspections/<int:insp_id>/edit', methods=['GET', 'POST'])
def edit_inspection(insp_id):
    """Show/ handle form to edit a specific inspection"""

    inspection = Inspection.query.get_or_404(insp_id)
    teams = [(t.id, t.team_name.title()) for t in Installation_team.query.all()]
    form = AddInspectionForm(obj=inspection)
    form.team_id.choices = teams

    if form.validate_on_submit():
        inspection.team_id = form.team_id.data
        inspection.sitter_id = form.sitter_id.data
        inspection.project_job_number = form.job_number.data
        inspection.date = form.date.data
        inspection.type = form.type.data
        inspection.result = form.result.data
        inspection.notes = form.notes.data
        inspection.to_close = form.to_close.data
        inspection.at_fault = form.at_fault.data

        db.session.commit()

        return redirect('/inspections')
    else:
        return render_template('/edit_inspection.html', form=form, inspection=inspection)

@app.route('/yesterdays_schedule')
def show_yesterdays_schedule():
    """Shows yesterday schedule"""

    schedule_date = date.today() - timedelta(days=1)
    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
    return render_template('schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/todays_schedule')
def show_todays_schedule():
    """Shows today schedule"""

    schedule_date = date.today()
    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
    return render_template('schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/tomorrows_schedule')
def show_tomorrows_schedule():
    """Shows tomorrows schedule"""

    schedule_date = date.today() + timedelta(days=1)
    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
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

@app.route("/building_depts/add", methods=['GET', 'POST'])
def handle_building_dept_form():
    """Handle adding new building department form"""

    form = AddBuildingDepartment()

    if form.validate_on_submit():
        state = form.state.data
        county = form.county.data
        city = form.city.data
        name = form.name.data
        rough_required = form.rough_required.data
        pe_cert_required = form.pe_cert_required.data
        type_of_pe_cert = form.type_of_pe_cert.data
        pe_cert_notes = form.pe_cert_notes.data
        shutdown_procedure = form.shutdown_procedure.data
        website = form.website.data
        inspection_portal = form.inspection_portal.data
        contact_list = form.contact_list.data
        notes = form.notes.data

        new_bd = Building_dept(state=state, 
                                county=county,
                                city=city,
                                name=name,
                                rough_required=rough_required,
                                pe_cert_required=pe_cert_required,
                                type_of_pe_cert=type_of_pe_cert,
                                shutdown_procedure=shutdown_procedure,
                                website=website,
                                inspection_portal=inspection_portal,
                                contact_list=contact_list,
                                notes=notes)

        db.session.add(new_bd)
        db.session.commit()
        return redirect("/building_depts")
    else:
        return render_template("add_building_dept.html", form=form)

@app.route('/building_depts/<int:bdid>')
def show_bd_details(bdid):
    """Show details on a specific building dept"""

    bd = Building_dept.query.get_or_404(bdid)
    return render_template('bd_details.html', bd=bd)

@app.route('/building_depts/<int:bdid>/edit', methods=['GET', 'POST'])
def show_edit_bd_form(bdid):
    """Show form to edit a specific building department"""

    bd = Building_dept.query.get_or_404(bdid)
    form = AddBuildingDepartment(obj=bd)

    if form.validate_on_submit():
        bd.state = form.state.data
        bd.county = form.county.data
        bd.city = form.city.data
        bd.name = form.name.data
        bd.rough_required = form.rough_required.data
        bd.pe_cert_required = form.pe_cert_required.data
        bd.type_of_pe_cert = form.type_of_pe_cert.data
        bd.pe_cert_notes = form.pe_cert_notes.data
        bd.shutdown_procedure = form.shutdown_procedure.data
        bd.website = form.website.data
        bd.inspection_portal = form.inspection_portal.data
        bd.contact_list = form.contact_list.data
        bd.notes = form.notes.data
        db.session.commit()
        return redirect(f'/building_depts/{bdid}')
    else:
        return render_template('edit_bd.html', form=form, bd=bd)

@app.route('/clients/<int:cid>')
def show_client_details(cid):
    """Show details on a specific client"""

    client = Client.query.get_or_404(cid)
    client_projects = Project.query.filter_by(client_id=cid).all()
    return render_template('client_details.html', client=client, client_projects=client_projects)

@app.route('/clients/add', methods=['GET', 'POST'])
def handle_client_form():
    """Show and handle add client form"""

    form = AddClient()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        notes = form.notes.data

        new_client = Client(first_name=first_name, last_name=last_name, notes=notes)
        db.session.add(new_client)
        db.session.commit()

        return redirect(f'/clients/{new_client.id}')
    else:
        return render_template('add_client.html', form=form)

@app.route('/projects/add', methods=['GET', 'POST'])
def handle_project_form():
    """Show and handle add project form for a specific client"""

    form = AddProject()
    building_depts = [(bd.id, bd.name.title()) for bd in Building_dept.query.all()]
    clients = [(c.id, c.get_full_name().title()) for c in Client.query.all()]
    form.bd_id.choices = building_depts
    form.client_id.choices = clients
    if form.validate_on_submit():
        client_id = form.client_id.data
        bd_id = form.bd_id.data
        job_number = form.job_number.data
        job_link = form.job_link.data
        description = form.description.data
        kws = form.kws.data

        new_project = Project(client_id=client_id, 
                                bd_id=bd_id, 
                                job_number=job_number, 
                                job_link=job_link, 
                                description=description,
                                kws = kws)
        db.session.add(new_project)
        db.session.commit()

        return redirect(f'/clients/{client_id}')
    else:
        return render_template('add_project.html', form=form)