from typing import Optional
from requests import get
from datetime import datetime, timedelta
import dateutil.parser
import pytz

from config import CLOCKIFY_TOKEN, CLOCKIFY_WID, CLOCKIFY_UID
import math

redmine_project_delimiter = 'redmine: '

api_url = 'https://api.clockify.me/api/v1/'


def get_redmine_project_name(entry) -> Optional[str]:
    project = entry.get('project')
    if project is not None:
        project_notes = project.get('note', '').splitlines()
        for project_note in project_notes:
            if redmine_project_delimiter in project_note:
                return project_note.lstrip(redmine_project_delimiter)

    return None


def get_date(time_entry) -> str:
    te_date = dateutil.parser.parse(time_entry.get('timeInterval').get('start'))
    return te_date.strftime('%Y-%m-%d')


def get_start_end(te) -> tuple:
    start = dateutil.parser.parse(te.get('timeInterval').get('start'))
    if te.get('timeInterval').get('end'):
        end = dateutil.parser.parse(te.get('timeInterval').get('end'))
    else:
        # end = datetime.now().replace(tzinfo=timezone('Canada/Eastern'))
        py = pytz.timezone('Canada/Eastern')
        end = datetime.now()
        end = py.localize(end)

    return start, end


def report(employee_id=None, iso_start=None, iso_end=None):
    if employee_id is None:
        employee_id = CLOCKIFY_UID
    if iso_start is None:
        iso_start = prior_week_end().isoformat() + 'Z'
    if iso_end is None:
        iso_end = datetime.utcnow().isoformat() + 'Z'
    r = get(
        api_url + f'workspaces/{CLOCKIFY_WID}/user/{employee_id}/time-entries',
        f'&start={iso_start}&end={iso_end}&hydrated=1',
        headers={'X-Api-Key': CLOCKIFY_TOKEN}
    )
    data = r.json()
    totals = {}
    for te in data:
        project_name = get_redmine_project_name(te)
        if project_name is not None:
            start, end = get_start_end(te)
            te_date = get_date(te)
            if project_name not in totals:
                totals[project_name] = {}
            if te_date not in totals[project_name]:
                totals[project_name][te_date] = timedelta()

            totals[project_name][te_date] = totals[project_name][te_date] + (end - start)

    return totals


def ceil(number):
    return math.ceil(number*100)/100


def prior_week_end():
    return datetime.utcnow() - timedelta(days=((datetime.now().isoweekday()) % 7))


def prior_week_start():
    return datetime.utcnow() - timedelta(weeks=1, days=(datetime.now().isoweekday()))

