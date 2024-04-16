from quickchart import QuickChart
from datetime import datetime, date, timedelta
from models import Inspection

qc = QuickChart()

def get_thirty_day_chart():
    """creates a pie chart breaking down the inspection results for trailing 30 days"""

    qc.width = 500
    qc.height = 300
    # qc.version = '2.9.4'

    inspections = Inspection.query.all()
    labels = ['Pending', 'Cancel', 'Fail', 'Partial', 'Pass', 'Rescheduled']
    t30 = date.today() - timedelta(days=30)
    
    pending = Inspection.query.filter(Inspection.result =='pending', Inspection.date > t30).count()
    cancel = Inspection.query.filter(Inspection.result =='cancel', Inspection.date > t30).count()
    fail = Inspection.query.filter(Inspection.result =='fail', Inspection.date > t30).count()
    partial = Inspection.query.filter(Inspection.result =='partial', Inspection.date > t30).count()
    passed = Inspection.query.filter(Inspection.result =='pass', Inspection.date > t30).count()
    resched = Inspection.query.filter(Inspection.result =='rescheduled', Inspection.date > t30).count()

# Config can be set as a string or as a nested dict
    qc.config = {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{ "data": [pending, cancel, fail, partial, passed, resched] }],
        },
    }

# return the chart URL...
    return qc.get_url()

def get_thirty_day_pass_fail_ratio():
    """Gets a ratio of the passed vs failed inspections for trailing 30 days"""

