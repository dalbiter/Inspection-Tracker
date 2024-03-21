""" Consider deletion behavior
    Double check constraints
    Double check relationships 
    Double check class name, table name, data type, nulls 
    Update docs with db design notes 
    Do models and schema png file match """

from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Building_dept(db.Model):
    """Building Deptartment"""

    __tablename__ = "building_depts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # use UUID
    state = db.Column(db.String(2), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rough_required = db.Column(db.Boolean)
    pe_cert_required = db.Column(db.Boolean)
    type_of_pe_cert = db.Column(db.String(50))
    pe_cert_notes = db.Column(db.Text)
    shutdown_procedure = db.Column(db.Text)
    website = db.Column(db.String)
    inspection_portal = db.Column(db.String)
    contact_list = db.Column(db.String) #link to contact list in Google drive or url
    notes = db.Column(db.Text)

    projects = db.relationship("Project", backref='building_dept')

    def __repr__(self):
        """Representation of building department"""

        bd = self
        return f"""Building_dept<building_dept id={bd.id}, 
                                               state={bd.state}, 
                                               county={bd.county},
                                               city={bd.city},
                                               name={bd.name},
                                               rough_required={bd.rough_required},
                                               pe_cert_required={bd.pe_cert_required},
                                               type_of_pe_cert={bd.type_of_pe_cert},
                                               shutdown_procedure={bd.shutdown_procedure},
                                               website={bd.website},
                                               inspection_portal={bd.inspection_portal},
                                               contact_list={bd.contact_list},
                                               notes={bd.notes}>"""
    
    @classmethod
    def get_bds_by_state(cls, state):
        """Takes a state abbreviation and returns a list of matching building departments"""

        return cls.query.filter(cls.state.ilike(f'%{state}%')).all()

class Client(db.Model):
    """Client"""

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text)

    projects = db.relationship("Project", backref='client')

    
    def get_full_name(self):
        return f"""{self.last_name.capitalize()}, {self.first_name.capitalize()}""" 

    def __repr__(self):
        """Representation of client"""

        c = self
        return f"Client<client id={c.id}, first_name={c.first_name}, last_name={c.last_name}>"

class Installation_team(db.Model):
    """Installation team"""

    __tablename__ = "installation_teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(100), nullable=False) #Ask Raf if we want team names or team leads 

    inspection = db.relationship("Inspection", backref='installation_team')

    def __repr__(self):
        """Representation of installation team"""

        t = self
        return f"Installation_team<installation_team id={t.id}, team_name={t.team_name}>"

class Project(db.Model):
    """Project"""

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))   
    bd_id = db.Column(db.Integer, db.ForeignKey('building_depts.id'))
    job_number = db.Column(db.Integer, nullable=False)
    job_link = db.Column(db.String)
    description = db.Column(db.String(150), nullable=False)
    kws = db.Column(db.Float)

    inspections = db.relationship("Inspection", backref='project')

    def __repr__(self):
        """Representation of project"""

        p = self
        return f"Project<project id={p.id}, client_id={p.client_id}, bd_id={p.bd_id}, job_number={p.job_number}, job_link={p.job_link}>"   

class Inspection(db.Model):
    """Inspection"""

    __tablename__ = "inspections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('installation_teams.id'), nullable=False)
    sitter_id = db.Column(db.Integer, db.ForeignKey('inspection_sitters.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(25), nullable=False, default='pending')
    notes = db.Column(db.Text)
    to_close = db.Column(db.Boolean, nullable=False, default=False)
    at_fault = db.Column (db.Boolean)

    def __repr__(self):
        """Representation of inspection"""

        i = self
        return f"""Inspection<inspection id={i.id}, 
                                         team_id={i.team_id}, 
                                         sitter_id={i.sitter_id},
                                         project_id={i.project_id},
                                         date={i.date},
                                         type={i.type},
                                         result={i.result},
                                         notes={i.notes},
                                         to_close={i.to_close},
                                         at_fault={i.at_fault}>"""

    @classmethod    
    def get_to_close(cls, team_id=None):
        """Takes a team_id and gets a list of all inspections that are 'to close'"""
        if(team_id):
            return cls.query.filter_by(to_close=True, team_id=team_id).all()
        else:
           return cls.query.filter_by(to_close=True).all()
    
    @classmethod
    def get_inspections(cls):
        """Returns a query object of inspection(s) ordered by project_id"""

        return cls.query.order_by(cls.project_id)
    
class Bd_contact(db.Model):
    """Building department Contact"""

    __tablename__ = "bd_contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bd_id = db.Column(db.Integer, db.ForeignKey('building_depts.id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(150))
    cell_phone = db.Column(db.String(20))
    office_phone = db.Column(db.String(20))
    email = db.Column(db.String(150))
    notes = db.Column(db.Text)

    def __repr__(self):
        """Representation of bd_contact"""

        bdc = self
        return f"""Bd_contact<bd_contact id={bdc.id}, 
                                         bd_id={bdc.bd_id}, 
                                         first_name={bdc.first_name},
                                         last_name={bdc.last_name},
                                         title={bdc.title},
                                         cell_phone={bdc.cell_phone},
                                         office_phone={bdc.office_phone},
                                         email={bdc.email},
                                         notes={bdc.notes}>"""
   
class Inspection_sitter(db.Model):
    """Inspection sitter"""

    __tablename__ = "inspection_sitters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))

    def __repr__(self):
        """Representation of inspection sitter"""

        s = self
        return f"Inspection_sitter<inspection_sitter id={s.id}, first_name={s.first_name}, last_name={s.last_name}, phone={s.phone}, email={s.email}>"