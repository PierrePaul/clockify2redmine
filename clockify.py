from requests import get
from datetime import datetime, timedelta
from pprint import PrettyPrinter
import dateutil.parser
import pytz

from config import CLOCKIFY_TOKEN, CLOCKIFY_WID, CLOCKIFY_UID
import math

pp = PrettyPrinter(indent=4)
api_url = 'https://api.clockify.me/api/v1/'


def pr(something):
    pp.pprint(something)


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
        client = 'No client'
        project = 'No project'
        if te.get('project') is not None:
            client = te.get('project').get('clientName', 'No client')
            project = te.get('project').get('name', 'No project')

        start = dateutil.parser.parse(te.get('timeInterval').get('start'))
        if te.get('timeInterval').get('end'):
            end = dateutil.parser.parse(te.get('timeInterval').get('end'))
        else:
            # end = datetime.now().replace(tzinfo=timezone('Canada/Eastern'))
            py = pytz.timezone('Canada/Eastern')
            end = datetime.now()
            end = py.localize(end)
        if client not in totals:
            totals[client] = {}
        if project not in totals[client]:
            totals[client][project] = timedelta()

        totals[client][project] = totals[client][project] + (end - start)

    return totals


def ceil(number):
    return math.ceil(number*100)/100


def prior_week_end():
    return datetime.utcnow() - timedelta(days=((datetime.now().isoweekday()) % 7))


def prior_week_start():
    return datetime.utcnow() - timedelta(weeks=1, days=(datetime.now().isoweekday()))

