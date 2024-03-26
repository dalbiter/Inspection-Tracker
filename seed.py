"""Seed file with sample data for inspection_tracker_db"""

from models import db, Building_dept, Client, Installation_team, Project, Inspection, Bd_contact, Inspection_sitter
from app import app

# create all tables 
db.drop_all()
db.create_all()

# add building dept

fll = Building_dept(state='fl', 
                    county='broward',
                    city='fort lauderdale', 
                    name='city of fort lauderdale',
                    rough_required=False,
                    pe_cert_required=True,
                    type_of_pe_cert='original/ wet stamp',
                    shutdown_procedure='schedule with fpl, and service rough with the city',
                    website='https://www.fortlauderdale.gov/government/departments-a-h/development-services/building-services',
                    inspection_portal='https://aca-prod.accela.com/FTL/Default.aspx',
                    contact_list='https://www.fortlauderdale.gov/government/departments-a-h/development-services/dsd-contacts')

miami = Building_dept(state='fl', 
                    county='miami dade',
                    city='miami dade', 
                    name='city of miami-dade',
                    rough_required=True,
                    pe_cert_required=False,
                    shutdown_procedure='schedule work with inspection with city, then shutdown with fpl, no inspection needed on day of shutdown',
                    website='https://www.miamidade.gov/global/economy/building/home.page',
                    inspection_portal='https://wwwx.miamidade.gov/Apps/RER/ePermittingMenu/Home/Permits')

pompano = Building_dept(state='fl', 
                    county='broward',
                    city='pompabo beach', 
                    name='city of pompano beach',
                    rough_required=False,
                    pe_cert_required=True,
                    type_of_pe_cert='original/ wet stamp',
                    shutdown_procedure='schedule with fpl, and service change with the city',
                    website='https://www.pompanobeachfl.gov/',
                    inspection_portal='https://www.pompanobeachfl.gov/government/building-inspections/inspection-scheduling-tracking',)

cobb = Building_dept(state='ga', 
                    county='cobb',
                    city='multiple', 
                    name='cobb county',
                    rough_required=False,
                    shutdown_procedure='schedule with utility, and service change with the city',
                    website='https://www.cobbcounty.org/community-development/building-development',
                    inspection_portal='https://cobbca.cobbcounty.org/CitizenAccess/default.aspx',)

mobile = Building_dept(state='al', 
                    county='mobile',
                    city='mobile', 
                    name='city of mobile',
                    rough_required=False,
                    shutdown_procedure='schedule with fpl, and service rough with the city',
                    website='https://www.buildmobile.org/',
                    inspection_portal='https://mobileal-energovpub.tylerhost.net/apps/selfservice#/home',)

# add clients

papa = Client(first_name='anthony', last_name='papagiorgiou', notes='Customer is having a pool built, and we need to wait until it is finished prior to inspections')
purcell = Client(first_name='claribel', last_name='purcell')
mcgee = Client(first_name='tad', last_name='mcgee')
king = Client(first_name='shamel', last_name='king', notes='customer will be out of town 4/17 - 4/21')
westerberg = Client(first_name='lennart', last_name='westerberg')

# add installation teams

nidel = Installation_team(team_name='nidel')
joe = Installation_team(team_name='joe')
yanick = Installation_team(team_name='yanick')
victor = Installation_team(team_name='victor')
hernan_p = Installation_team(team_name='hernan p')

# add projects
# don't forget to check bd_id is correct and add field status (open or closed)
p_papa = Project(client_id=1, bd_id=1, job_number=23117251, job_link='https://app.jobnimbus.com/job/lp1a796rbav5uk8agr3kbgh', description='Solar and Powerwalls', kws=14.58)
p_papa2 = Project(client_id=1, bd_id=1, job_number=24017434, job_link='https://app.jobnimbus.com/job/lrjbr2n9j8e2iv2hnlroc4n', description='additional Powerwalls')
p_purcell = Project(client_id=2, bd_id=2, job_number=23107156, job_link='https://app.jobnimbus.com/job/lnytimj65kmw94qwau9frrh', description='Solar and Powerwalls', kws=11.75)
p_mcgee = Project(client_id=3, bd_id=3, job_number=23117279, job_link='https://app.jobnimbus.com/job/lph4l58w1o0w0ftok4ja6s0', description='Solar and Powerwalls', kws=25.51)
p_mcgee2 = Project(client_id=3, bd_id=3, job_number=24027518, job_link='https://app.jobnimbus.com/job/lsj7gztnssyz40idpdw370', description='Additional panels', kws=7.29)
p_king = Project(client_id=4, bd_id=4, job_number=22054674, job_link='https://app.jobnimbus.com/job/l3c4g756b63qepx65ppjzwh', description='Solar and Powerwalls', kws=13.34)
p_westerberg = Project(client_id=5, bd_id=5, job_number=23107198, job_link='https://app.jobnimbus.com/job/loemwhurezhn77qcv9qspeq', description='Solar and Powerwalls', kws=11.46)

# add inspections

i_papa = Inspection(team_id=1, 
                    project_job_number=23117251,
                    date='2024-03-24',
                    type='service change')

i_purcell = Inspection(team_id=1, 
                    sitter_id=1,
                    project_job_number=23107156,
                    date='2024-03-25',
                    type='final electrical',
                    result='pass',
                    to_close=True)

i_mcgee = Inspection(team_id=1, 
                    project_job_number=23117279,
                    date='2024-03-25',
                    type='rough electrical')

i_king = Inspection(team_id=2, 
                    project_job_number=22054674,
                    date='2024-03-26',
                    type='final electrical',
                    notes='final building after, but there may also be a final fire inspection')

i_king2 = Inspection(team_id=2, 
                    project_job_number=22054674,
                    date='2024-03-25',
                    type='rough electrical',
                    notes='final building after, but there may also be a final fire inspection')

i_westerberg = Inspection(team_id=1, 
                    project_job_number=23107198,
                    date='2024-03-26',
                    type='final electrical',
                    result='fail',
                    notes='need tech on site',
                    at_fault=True)

# add bd contacts
#check bd_ids
ron = Bd_contact(bd_id=1, 
                 first_name='ronald',
                 last_name='smith',
                 title='electrical inspector',
                 office_phone='786-315-2268',
                 email='E404057@miamidade.gov')

sal = Bd_contact(bd_id=2, 
                 first_name='sal',
                 last_name='munson',
                 title='structural inspector',
                 cell_phone='561-555-1234',
                 office_phone='561-555-4321',
                 email='sal@inspector.com')

# add inspection sitters

jairo = Inspection_sitter(first_name='jairo',
                          last_name='cure',
                          phone='786-800-6814',
                          email='jairo@gosolarpower.com')

#add and commit all building depts
db.session.add_all([fll, miami, pompano, cobb, mobile])
db.session.commit()

#add and commit all clients
db.session.add_all([papa, purcell, mcgee, king, westerberg])
db.session.commit()

#add and commit all installation teams
db.session.add_all([nidel, joe, yanick, victor, hernan_p])
db.session.commit()

#add and commit all projects
db.session.add_all([p_papa, p_papa2, p_purcell, p_mcgee, p_mcgee2, p_king, p_westerberg])
db.session.commit()

#add and commit all inspection sitters
db.session.add(jairo)
db.session.commit()

#add and commit all inspections
db.session.add_all([i_papa, i_purcell, i_mcgee, i_king, i_king2, i_westerberg])
db.session.commit()

#add and commit all bd contacts
db.session.add_all([ron, sal])
db.session.commit()