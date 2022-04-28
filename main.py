from clockify import report
from redmine import get_time_entries, init_redmine
from utils import pr

init_redmine()
clockify_entries = report()
clockify_entries_formatted = {}
for project_name, entries in clockify_entries.items():
    for date_, task in entries.items():
        for task_id, total in task.items():
            hours, remainder = divmod(total.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            total_formatted = hours + round(minutes/60, 2)
            redmine_entries = get_time_entries(str(task_id), date_)
            pr(redmine_entries)
