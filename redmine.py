import requests
from pomerium import get_pomerium_cookie
from config import REDMINE_URL, REDMINE_TOKEN, REDMINE_UID
from utils import pr

s = requests.session()


def init_redmine():
    pomerium_cookie = get_pomerium_cookie()
    s.cookies.set('_pomerium', pomerium_cookie.get('value'), domain=pomerium_cookie.get('domain'))
    s.auth = (REDMINE_TOKEN, 'random')


def get_time_entries(task_id: str, date_: str) -> list:
    response = s.get(
        REDMINE_URL + f'/time_entries.json?task_id={task_id}&user_id={str(REDMINE_UID)}&spent_on={date_}',
    )
    return response.json().get('time_entries')
