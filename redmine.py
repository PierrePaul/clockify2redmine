import requests
from dateutil import parser
from pomerium import get_pomerium_cookie
from config import REDMINE_URL, REDMINE_TOKEN, REDMINE_UID
from datetime import timedelta
from utils import pr

s = requests.session()


def init_redmine():
    pomerium_cookie = get_pomerium_cookie()
    s.cookies.set('_pomerium', pomerium_cookie.get('value'), domain=pomerium_cookie.get('domain'))
    s.auth = (REDMINE_TOKEN, 'random')


def get_time_entries(date_start: str, date_end: str) -> list:
    response = s.get(
        REDMINE_URL + f'/time_entries.json?user_id={str(REDMINE_UID)}&from={date_start}&to={date_end}',
    )
    print(REDMINE_URL + f'/time_entries.json?user_id={str(REDMINE_UID)}&from={date_start}&to={date_end}')
    return response.json().get('time_entries')

def redmine_format(redmine_entries: list):
    ex = [{
        'comments': 'Autosync clockify',                                                                                                
        'created_on': '2022-04-29T15:28:00Z',
        'hours': 0.58,                                              
        'id': 222016,                                               
        'issue': {'id': 34943},                                     
        'project': {'id': 504, 'name': 'BANQ-22-01-BLD LyXn portal build'},
        'spent_on': '2022-04-28',                                   
        'updated_on': '2022-04-29T15:28:00Z',
        'user': {'id': 183, 'name': 'Pierre-Paul Lefebvre'}}]

    formatted_entries = {}
    for entry in redmine_entries:
        date_ = parser.parse(entry.get('spent_on')).strftime('%Y-%m-%d')
        project_id = entry.get('project', {}).get('id')
        task_id = entry.get('issue', {}).get('id')
        user_id = entry.get('user', {}).get('id')
        if str(user_id) == REDMINE_UID:
            if project_id not in formatted_entries:
                formatted_entries[project_id] = {}
            if date_ not in formatted_entries[project_id]:
                formatted_entries[project_id][date_] = {}
            if task_id not in formatted_entries[project_id][date_]:
                formatted_entries[project_id][date_][task_id] = 0

            formatted_entries[project_id][date_][task_id] += entry.get('hours')

    pr(formatted_entries)
    return formatted_entries
