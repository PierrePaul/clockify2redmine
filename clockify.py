import logging
from typing import Optional
from logging import log
from requests import get
from datetime import datetime
from utils import get_date,prior_week_end, get_start_end
import re

from config import CLOCKIFY_TOKEN, CLOCKIFY_WID, CLOCKIFY_UID

redmine_project_delimiter = 'redmine: '

api_url = 'https://api.clockify.me/api/v1/'


def get_redmine_project_name(entry) -> Optional[int]:
    project = entry.get('project')
    if project is not None:
        project_notes = project.get('note', '').splitlines()
        for project_note in project_notes:
            if redmine_project_delimiter in project_note:
                return int(project_note.lstrip(redmine_project_delimiter))

    return None


def get_task_id(entry) -> Optional[int]:
    description = entry.get('description')
    matches = re.search(r'#(\d+)', description)
    if matches is not None:
        return int(matches.group(1))

    return None


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
            task_id = get_task_id(te)
            start, end = get_start_end(te)
            te_date = get_date(te)

            if task_id is None:
                log(logging.ERROR, f"At least one clockify time entry from project {project_name} on date {te_date} has no task_id associated.")
            else:
                # We want to end up with totals[my_project][2022-01-01][12341] = 0
                if project_name not in totals:
                    totals[project_name] = {}
                if te_date not in totals[project_name]:
                    totals[project_name][te_date] = {}
                if task_id not in totals[project_name][te_date]:
                    totals[project_name][te_date][task_id] = 0

                total = end - start
                hours, remainder = divmod(total.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                total_formatted = hours + round(minutes/60, 2)
                totals[project_name][te_date][task_id] += total_formatted

    return totals
