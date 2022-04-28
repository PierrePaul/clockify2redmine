import requests
from pomerium import get_pomerium_cookie
from config import REDMINE_URL, REDMINE_TOKEN, REDMINE_UID
from utils import pr

pomerium_cookie = get_pomerium_cookie()
s = requests.session()
s.cookies.set('_pomerium', pomerium_cookie.get('value'), domain=pomerium_cookie.get('domain'))
s.auth = (REDMINE_TOKEN, 'random')


def get_time_entries(project_name: str) -> list:
    response = s.get(
        REDMINE_URL + f'/time_entries.json?project_id={project_name}&user_id={str(REDMINE_UID)}',
    )
    return response.json().get('time_entries')
