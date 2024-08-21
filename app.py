"""review queries to be sure using new convention db.session.execute(db.select())"""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Building_dept, Client, Installation_team, Project, Inspection, Bd_contact, Inspection_sitter
from sqlalchemy import text
from datetime import datetime, date, timedelta
from forms import AddBuildingDepartment, AddClient, AddInstallationTeam, AddProject, AddInspectionForm, AddBdContact, AddInspectionSitter
from charts import get_thirty_day_chart

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

# building departments routes 
@app.route('/building_depts')
def show_building_depts():
    """Show building depts landing page"""

    building_depts = db.session.execute(db.select(Building_dept).order_by(Building_dept.name)).scalars()
    return render_template('building_depts/building_depts.html', building_depts=building_depts)

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
                                pe_cert_notes=pe_cert_notes,
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
        return render_template("building_depts/add_building_dept.html", form=form)

@app.route('/building_depts/<int:bdid>')
def show_bd_details(bdid):
    """Show details on a specific building dept"""

    bd = Building_dept.query.get_or_404(bdid)
    return render_template('building_depts/bd_details.html', bd=bd)

@app.route('/building_depts/<int:bdid>/edit', methods=['GET', 'POST'])
def edit_bduilding_dept(bdid):
    """Show and handle form to edit a building department"""

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
        return render_template('building_depts/edit_bd.html', form=form, bd=bd)

# clients routes
@app.route('/clients')
def show_clients():
    """Show list of clients"""

    clients = db.session.execute(db.select(Client).order_by(Client.last_name)).scalars()
    return render_template('clients/clients.html', clients=clients)

@app.route('/clients/<int:cid>')
def show_client_details(cid):
    """Show details on a specific client"""

    client = Client.query.get_or_404(cid)
    client_projects = Project.query.filter_by(client_id=cid).all()
    return render_template('clients/client_details.html', client=client, client_projects=client_projects)

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
        return render_template('clients/add_client.html', form=form)

@app.route('/clients/<int:cid>/edit', methods=['GET', 'POST'])
def edit_client(cid):
    """Show and handle form to edit a client"""

    client = Client.query.get_or_404(cid)
    form = AddClient(obj=client)

    if form.validate_on_submit():
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data
        client.notes = form.notes.data

        db.session.commit()
        return redirect(f'/clients/{client.id}')
    else:
        return render_template('clients/edit_client.html', form=form, client=client)

# installation teams routes
@app.route('/installation_teams')
def show_install_teams():
    """Show list of all installation teams"""

    teams = db.session.execute(db.select(Installation_team).order_by(Installation_team.team_name)).scalars()
    return render_template('installation_teams/install_teams.html', teams=teams) 

@app.route('/installation_teams/<int:tid>')
def show_install_team(tid):
    """Show details on installation team"""

    team = Installation_team.query.get_or_404(tid)
    thirty_day_chart = get_thirty_day_chart()

    return render_template('installation_teams/install_team_details.html', team=team, thirty_day_chart=thirty_day_chart)

@app.route('/installation_teams/add', methods=['GET', 'POST'])
def handle_install_team_form():

    form = AddInstallationTeam()

    if form.validate_on_submit():
        team_name = form.team_name.data

        new_team = Installation_team(team_name=team_name)
        db.session.add(new_team)
        db.session.commit()
        return redirect(f'/installation_teams/{new_team.id}')
    else:
        return render_template('installation_teams/add_install_team.html', form=form)

@app.route('/installation_teams/<int:tid>/edit', methods=['GET', 'POST'])
def edit_install_team(tid):
    """Show and handle edit install team form"""

    team = Installation_team.query.get_or_404(tid)
    form = AddInstallationTeam(obj=team)

    if form.validate_on_submit():
        team.team_name = form.team_name.data

        db.session.commit()
        return redirect(f'/installation_teams/{team.id}')
    else:
        return render_template('installation_teams/edit_install_team.html', form=form, team=team)

# projects routes
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
        notes = form.notes.data

        new_project = Project(client_id=client_id, 
                                bd_id=bd_id, 
                                job_number=job_number, 
                                job_link=job_link, 
                                description=description,
                                kws=kws,
                                notes=notes)
        db.session.add(new_project)
        db.session.commit()

        return redirect(f'/clients/{client_id}')
    else:
        return render_template('projects/add_project.html', form=form)

@app.route('/projects/<int:pid>')
def show_project_details(pid):
    """Show project details"""

    project = Project.query.get_or_404(pid)

    return render_template('projects/project_details.html', project=project)
    
@app.route('/projects/<int:pid>/edit', methods=['GET', 'POST'])
def edit_project(pid):
    """Show and handle edit project form"""

    project = Project.query.get_or_404(pid)
    clients = [(c.id, c.get_full_name().title()) for c in Client.query.all()]
    building_depts = [(bd.id, bd.name.title()) for bd in Building_dept.query.all()]
    form = AddProject(obj=project)
    form.client_id.choices = clients
    form.bd_id.choices = building_depts

    if form.validate_on_submit():
        project.client_id = form.client_id.data
        project.bd_id = form.bd_id.data
        project.job_number = form.job_number.data
        project.job_link = form.job_link.data
        project.description = form.description.data
        project.kws = form.kws.data
        project.notes = form.notes.data 

        db.session.commit()
        
        return redirect(f'/projects/{pid}')
    else:
        return render_template('projects/edit_project.html', form=form, project=project)

# inspections routes
@app.route('/inspections')
def show_inspection_scheduling():
    """Show inspection scheduling options"""

    return render_template('inspections/inspections.html')

@app.route('/inspections/add', methods=['GET', 'POST'])
def handle_inspection_form():
    """Handles form to add a new inspection instance"""

    form = AddInspectionForm()
    teams = [(t.id, t.team_name.title()) for t in Installation_team.query.all()]
    sitters = [(s.id, s.get_full_name().title()) for s in Inspection_sitter.query.all()]
    form.team_id.choices = teams
    form.sitter_id.choices = sitters

    if form.validate_on_submit():
        team_id = form.team_id.data
        sitter_id = form.sitter_id.data
        project_job_number = form.project_job_number.data
        date = form.date.data
        type = form.type.data
        result = form.result.data
        notes = form.notes.data
        to_close = form.to_close.data
        at_fault = form.at_fault.data

        team = Installation_team.query.get_or_404(team_id)
        new_inspection = Inspection(team_id=team_id, 
                                    sitter_id=sitter_id, 
                                    project_job_number=project_job_number, 
                                    date=date, type=type, 
                                    result=result, notes=notes, 
                                    to_close=to_close, 
                                    at_fault=at_fault)
        db.session.add(new_inspection)
        db.session.commit()

        flash(f'Created new inspection for team: {team.team_name.title()} on {date}')
        return redirect('/inspections')
    else:
        return render_template('inspections/add_inspection.html', form=form)
    
@app.route('/inspections/<int:insp_id>/edit', methods=['GET', 'POST'])
def edit_inspection(insp_id):
    """Show and handle form to edit an inspection"""

    inspection = Inspection.query.get_or_404(insp_id)
    teams = [(t.id, t.team_name.title()) for t in Installation_team.query.all()]
    sitters = [(s.id, s.get_full_name().title()) for s in Inspection_sitter.query.all()]
    form = AddInspectionForm(obj=inspection)
    form.team_id.choices = teams
    form.sitter_id.choices = sitters

    if form.validate_on_submit():
        inspection.team_id = form.team_id.data
        inspection.sitter_id = form.sitter_id.data
        inspection.project_job_number = form.project_job_number.data
        inspection.date = form.date.data
        inspection.type = form.type.data
        inspection.result = form.result.data
        inspection.notes = form.notes.data
        inspection.to_close = form.to_close.data
        inspection.at_fault = form.at_fault.data

        team = Installation_team.query.get_or_404(inspection.team_id)

        db.session.commit()
        flash(f'Updated inspection for team: {team.team_name.title()} on {inspection.date}')

        return redirect('/inspections')
    else:
        return render_template('inspections/edit_inspection.html', form=form, inspection=inspection)
    
@app.route('/inspections/<int:insp_id>/delete', methods=['POST'])
def delete_inspection(insp_id):
    """Delete a specific inspection instance"""

    Inspection.query.filter_by(id=insp_id).delete()
    db.session.commit()
    return redirect('/inspections')

@app.route('/yesterdays_schedule')
def show_yesterdays_schedule():
    """Shows yesterday schedule"""

    if date.weekday(date.today()) == 0:
        schedule_date = date.today() - timedelta(days=3)       
    else:
        schedule_date = date.today() - timedelta(days=1)

    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
    return render_template('inspections/schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/todays_schedule')
def show_todays_schedule():
    """Shows today schedule"""

    schedule_date = date.today()
    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
    return render_template('inspections/schedule.html', schedule_date=schedule_date, inspections=inspections)

@app.route('/tomorrows_schedule')
def show_tomorrows_schedule():
    """Shows tomorrows schedule"""

    if date.weekday(date.today()) == 4:
        schedule_date = date.today() + timedelta(days=3)       
    else:
        schedule_date = date.today() + timedelta(days=1)

    inspections = Inspection.get_inspections().filter(Inspection.date==schedule_date).all()
    return render_template('inspections/schedule.html', schedule_date=schedule_date, inspections=inspections)    

# building dept contacts routes
@app.route('/building_depts/<int:bdid>/contacts')
def show_bd_contacts(bdid):
    """Show building department contacts for a specific building department"""

    contacts = Bd_contact.query.filter_by(bd_id=bdid).all()
    building_dept = Building_dept.query.get_or_404(bdid)

    return render_template('bd_contacts/bd_contacts.html', contacts=contacts, building_dept=building_dept)

@app.route('/bd_contacts/<int:cid>')
def show_bd_contact_details(cid):

    contact = Bd_contact.query.get_or_404(cid)
    return render_template('bd_contacts/bd_contact_details.html', contact=contact)

@app.route('/bd_contacts/add', methods=['GET', 'POST'])
def handle_add_bd_contact():
    """Show and handle add building department contact form"""

    building_depts = [(bd.id, bd.name.title()) for bd in Building_dept.query.all()]
    form = AddBdContact()
    form.bd_id.choices = building_depts

    if form.validate_on_submit():
        bd_id = form.bd_id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        title = form.title.data
        cell_phone = form.cell_phone.data
        office_phone = form.office_phone.data
        email = form.email.data
        notes = form.notes.data

        new_contact = Bd_contact(bd_id=bd_id,
                                first_name=first_name,
                                last_name=last_name,
                                title=title,
                                cell_phone=cell_phone,
                                office_phone=office_phone,
                                email=email,
                                notes=notes)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(f'/bd_contacts/{new_contact.id}')
    else:
        return render_template('bd_contacts/add_bd_contact.html', form=form)
    
@app.route('/bd_contacts/<int:cid>/edit', methods=['GET', 'POST'])
def edit_bd_contact(cid):
    """Show and handle edit building dept contact form"""

    contact = Bd_contact.query.get_or_404(cid)
    building_depts = [(bd.id, bd.name.title()) for bd in Building_dept.query.all()]
    form = AddBdContact(obj=contact)
    form.bd_id.choices = building_depts

    if form.validate_on_submit():
        contact.bd_id = form.bd_id.data
        contact.first_name = form.first_name.data
        contact.last_name = form.last_name.data
        contact.title = form.title.data
        contact.cell_phone = form.cell_phone.data
        contact.office_phone = form.office_phone.data
        contact.email = form.email.data
        contact.notes = form.notes.data 

        db.session.commit()
        return redirect(f'/bd_contacts/{cid}')
    else:
        return render_template('bd_contacts/edit_bd_contact.html', form=form, contact=contact)

# sitters routes routes
@app.route('/inspection_sitters')
def show_inspection_sitters():
    """Show list of all inspection sitters"""

    sitters = Inspection_sitter.query.all()
    return render_template('inspection_sitters/inspection_sitters.html', sitters=sitters)

@app.route('/inspection_sitters/<int:sid>')
def show_inspection_sitter_details(sid):
    """Show details for specific inspection sitter instance"""
    
    sitter = Inspection_sitter.query.get_or_404(sid)
    return render_template('inspection_sitters/inspection_sitter_details.html', sitter=sitter)

@app.route('/inspection_sitters/add', methods=['GET', 'POST'])
def handle_add_inspection_sitter():
    """Show and handle add inspection sitter form"""

    form = AddInspectionSitter()
        
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data

        new_sitter = Inspection_sitter(first_name=first_name, last_name=last_name, phone=phone, email=email)
        db.session.add(new_sitter)
        db.session.commit()
        return redirect(f'/inspection_sitters/{new_sitter.id}')
    else:
        return render_template('inspection_sitters/add_inspection_sitter.html', form=form)
    
@app.route('/inspection_sitters/<int:sid>/edit', methods=['GET', 'POST'])
def edit_inspection_sitter(sid):
    """Show and handle edit inspection sitter form"""

    sitter = Inspection_sitter.query.get_or_404(sid)
    form = AddInspectionSitter(obj=sitter)

    if form.validate_on_submit():
        sitter.first_name = form.first_name.data
        sitter.last_name = form.last_name.data
        sitter.phone = form.phone.data
        sitter.email = form.email.data

        db.session.commit()
        return redirect(f'/inspection_sitters/{sitter.id}')
    else:
        return render_template('inspection_sitters/edit_inspection_sitter.html', form=form, sitter=sitter)

# Views related to dashboard and reporting

@app.route('/dashboard')
def show_dashboard():
    """Show inspections dashboard"""

    thirty_day_chart = get_thirty_day_chart()

    return render_template('dashboard.html', thirty_day_chart=thirty_day_chart)

@app.route('/update_db')
def show_update_db_menu():
    """Shows landing page for updating database"""

    return render_template('update_db.html')