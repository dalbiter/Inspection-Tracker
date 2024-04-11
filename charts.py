from quickchart import QuickChart
from datetime import datetime, date, timedelta
from models import Inspection

qc = QuickChart()

def get_chart():
    qc.width = 500
    qc.height = 300
    # qc.version = '2.9.4'

    inspections = Inspection.query.all()
    labels = ['Pending', 'Cancel', 'Fail', 'Partial', 'Pass', 'Rescheduled']
    data = Inspection.query

# Config can be set as a string or as a nested dict
    qc.config = {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{ "data": [50, 60, 70, 180, 190, 120] }],
        },
    }

# return the chart URL...
    return qc.get_url()

